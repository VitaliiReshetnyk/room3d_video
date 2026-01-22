from pathlib import Path
import open3d as o3d


def view_geometry(path: str) -> None:
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(str(p))

    if p.suffix.lower() in [".ply", ".pcd", ".xyz", ".xyzn", ".xyzrgb"]:
        g = o3d.io.read_point_cloud(str(p))
        if g.is_empty():
            raise RuntimeError("Empty point cloud.")
        o3d.visualization.draw_geometries([g])
        return

    if p.suffix.lower() in [".obj", ".stl", ".off", ".gltf", ".glb", ".ply"]:
        m = o3d.io.read_triangle_mesh(str(p))
        if m.is_empty():
            raise RuntimeError("Empty mesh.")
        if not m.has_vertex_normals():
            m.compute_vertex_normals()
        o3d.visualization.draw_geometries([m])
        return

    raise ValueError(f"Unsupported format: {p.suffix}")
