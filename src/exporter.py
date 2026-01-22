from pathlib import Path
import open3d as o3d


def export_mesh(input_mesh_path: str, out_path: str) -> str:
    inp = Path(input_mesh_path).resolve()
    out = Path(out_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    mesh = o3d.io.read_triangle_mesh(str(inp))
    if mesh.is_empty():
        raise RuntimeError("Empty mesh.")
    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()

    ok = o3d.io.write_triangle_mesh(str(out), mesh, write_ascii=False, compressed=True)
    if not ok:
        raise RuntimeError(f"Failed to write: {out}")
    return str(out)


def export_point_cloud(input_ply_path: str, out_path: str) -> str:
    inp = Path(input_ply_path).resolve()
    out = Path(out_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    pcd = o3d.io.read_point_cloud(str(inp))
    if pcd.is_empty():
        raise RuntimeError("Empty point cloud.")

    ok = o3d.io.write_point_cloud(str(out), pcd, write_ascii=False, compressed=True)
    if not ok:
        raise RuntimeError(f"Failed to write: {out}")
    return str(out)
