import os
import shutil
import subprocess
from pathlib import Path

import cv2


def extract_frames(mp4_path: str, out_dir: str, fps: float | None = None, max_frames: int | None = None) -> None:
    mp4_path = str(Path(mp4_path).resolve())
    out_dir_p = Path(out_dir).resolve()
    out_dir_p.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(mp4_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {mp4_path}")

    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    step = 1
    if fps is not None and fps > 0:
        step = max(1, int(round(src_fps / fps)))

    i = 0
    saved = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if i % step == 0:
            saved += 1
            cv2.imwrite(str(out_dir_p / f"frame_{saved:06d}.jpg"), frame)
            if max_frames is not None and saved >= max_frames:
                break
        i += 1
    cap.release()


def _run(cmd: list[str]) -> None:
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = []
    assert p.stdout is not None
    for line in p.stdout:
        print(line, end="")
        out.append(line)
    rc = p.wait()
    if rc != 0:
        raise RuntimeError("".join(out))


def colmap_reconstruct(frames_dir: str, work_dir: str) -> dict:
    import os
    from pathlib import Path

    frames_dir = str(Path(frames_dir).resolve())
    work = Path(work_dir).resolve()
    work.mkdir(parents=True, exist_ok=True)

    db_path = str(work / "database.db")
    sparse_dir = work / "sparse"
    dense_dir = work / "dense"
    sparse_dir.mkdir(exist_ok=True)
    dense_dir.mkdir(exist_ok=True)

    if os.path.exists(db_path):
        os.remove(db_path)

    print(f"[COLMAP] frames_dir = {frames_dir}")
    print(f"[COLMAP] work_dir   = {work}")
    print(f"[COLMAP] database   = {db_path}")

    print("[1/6] feature_extractor ...")
    _run(["colmap", "feature_extractor", "--database_path", db_path, "--image_path", frames_dir])

    print("[2/6] exhaustive_matcher ...")
    _run(["colmap", "exhaustive_matcher", "--database_path", db_path])

    print("[3/6] mapper (sparse SfM) ...")
    _run([
        "colmap", "mapper",
        "--database_path", db_path,
        "--image_path", frames_dir,
        "--output_path", str(sparse_dir),
    ])

    sparse0 = sparse_dir / "0"
    if not sparse0.exists() or len(list(sparse0.glob("*"))) == 0:
        raise RuntimeError("COLMAP mapper produced no model. Try better video / more overlap / better lighting.")

    print("[4/6] image_undistorter (prepare dense workspace) ...")
    _run([
        "colmap", "image_undistorter",
        "--image_path", frames_dir,
        "--input_path", str(sparse0),
        "--output_path", str(dense_dir),
        "--output_type", "COLMAP",
    ])

    print("[5/6] patch_match_stereo (dense depth) ...")
    _run([
        "colmap", "patch_match_stereo",
        "--workspace_path", str(dense_dir),
        "--workspace_format", "COLMAP",
    ])

    fused_ply = dense_dir / "fused.ply"
    print("[6/6] stereo_fusion -> fused point cloud ...")
    _run([
        "colmap", "stereo_fusion",
        "--workspace_path", str(dense_dir),
        "--workspace_format", "COLMAP",
        "--input_type", "geometric",
        "--output_path", str(fused_ply),
    ])

    mesh_ply = dense_dir / "mesh_poisson.ply"
    print("[6/6] poisson_mesher -> mesh ...")
    _run([
        "colmap", "poisson_mesher",
        "--input_path", str(fused_ply),
        "--output_path", str(mesh_ply),
    ])

    if not fused_ply.exists():
        raise RuntimeError(f"Expected point cloud not found: {fused_ply}")
    if not mesh_ply.exists():
        raise RuntimeError(f"Expected mesh not found: {mesh_ply}")

    print("[COLMAP] DONE")
    print(f"[COLMAP] fused_ply = {fused_ply}")
    print(f"[COLMAP] mesh_ply  = {mesh_ply}")

    return {
        "work_dir": str(work),
        "frames_dir": frames_dir,
        "sparse_model": str(sparse0),
        "dense_fused_ply": str(fused_ply),
        "mesh_ply": str(mesh_ply),
    }
