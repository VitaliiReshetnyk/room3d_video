import argparse
from pathlib import Path

from pipeline import extract_frames, colmap_reconstruct
from viewer import view_geometry
from exporter import export_mesh, export_point_cloud


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--work", default="work")
    ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--max_frames", type=int, default=800)
    ap.add_argument("--view", action="store_true")
    ap.add_argument("--export_dir", default="exports")
    args = ap.parse_args()

    work = Path(args.work).resolve()
    frames = work / "frames"

    extract_frames(args.video, str(frames), fps=args.fps, max_frames=args.max_frames)
    result = colmap_reconstruct(str(frames), str(work))

    export_dir = Path(args.export_dir).resolve()
    export_dir.mkdir(parents=True, exist_ok=True)

    mesh_out_obj = export_mesh(result["mesh_ply"], str(export_dir / "room.obj"))
    mesh_out_glb = export_mesh(result["mesh_ply"], str(export_dir / "room.glb"))
    pcd_out_ply = export_point_cloud(result["dense_fused_ply"], str(export_dir / "room_pointcloud.ply"))

    print("OK")
    print("Mesh (OBJ):", mesh_out_obj)
    print("Mesh (GLB):", mesh_out_glb)
    print("PointCloud (PLY):", pcd_out_ply)

    if args.view:
        view_geometry(result["mesh_ply"])


if __name__ == "__main__":
    main()

