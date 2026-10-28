import time
import threading
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import os
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

if sim.getSimulationState() == sim.simulation_stopped:
    sim.startSimulation()

time.sleep(1.0)

# 1. AMBIL HANDLE OBJEK
quad = sim.getObject('/Quadcopter')

target = -1
for path in ['/target', 'target', './target', '/Quadcopter/target']:
    try:
        target = sim.getObject(path)
        if target != -1: break
    except Exception: pass

sensor = -1
for path in ['/Quadcopter/fast3DLaserScanner', '/fast3DLaserScanner', '/Quadcopter/3DLaserScanner']:
    try:
        sensor = sim.getObject(path)
        if sensor != -1: break
    except Exception: pass

print(f"[DEBUG] Quadcopter Handle : {quad}")
print(f"[DEBUG] Target Handle     : {target}")
print(f"[DEBUG] Sensor Handle     : {sensor}")

pos_awal = sim.getObjectPosition(quad, -1)
cmd_pos = [pos_awal[0], pos_awal[1], pos_awal[2]]
sim.setObjectPosition(target, -1, cmd_pos)

pts_data = []
trajectory = []
is_running = True

active_keys = set()
speed = 0.08


def update_loop():
    global is_running, cmd_pos
    while is_running:
        if sim.getSimulationState() == sim.simulation_stopped:
            is_running = False
            break

        # Controller pergerakan
        dx, dy, dz = 0.0, 0.0, 0.0
        if 'w' in active_keys: dy += speed
        if 's' in active_keys: dy -= speed
        if 'a' in active_keys: dx -= speed
        if 'd' in active_keys: dx += speed
        if 'i' in active_keys: dz += speed
        if 'k' in active_keys: dz -= speed

        if dx != 0 or dy != 0 or dz != 0:
            cmd_pos[0] += dx
            cmd_pos[1] += dy
            cmd_pos[2] += dz
            sim.setObjectPosition(target, -1, cmd_pos)

        # Record trajectory
        p_now = sim.getObjectPosition(quad, -1)
        trajectory.append(p_now)

        # BACA SEMUA KEMUNGKINAN NAMA SIGNAL BUFFER
        raw = sim.getBufferSignal("fast3D_data")
        if not raw or len(raw) == 0:
            raw = sim.getBufferSignal("measuredDataAtThisTime")
        if not raw or len(raw) == 0:
            raw = sim.getBufferSignal("fast3DLaserScanner_data")

        if raw and len(raw) > 0:
            try:
                m = sim.getObjectMatrix(sensor, -1)
                T = np.eye(4)
                T[:3, :4] = np.array(m).reshape(3, 4)

                loc_pts = np.frombuffer(raw, dtype=np.float32).reshape(-1, 3)
                if len(loc_pts) > 0:
                    ones = np.ones((loc_pts.shape[0], 1), dtype=np.float32)
                    pts_h = np.hstack([loc_pts, ones])
                    glob_pts = (T @ pts_h.T).T[:, :3]

                    for p in glob_pts:
                        if -10.0 < p[0] < 10.0 and -10.0 < p[1] < 10.0 and -0.05 < p[2] < 5.0:
                            pts_data.append(p)
            except Exception as e:
                pass

        time.sleep(0.02)

t_loop = threading.Thread(target=update_loop, daemon=True)
t_loop.start()


def close_app():
    global is_running
    is_running = False
    root.destroy()


# GUI CONTROLLER
root = tk.Tk()
root.title("Drone Controller")
root.geometry("340x380")
root.attributes('-topmost', True)

lbl = tk.Label(root, text="Quadcopter Flight Control", font=("Helvetica", 11, "bold"))
lbl.pack(pady=8)

nav_frame = tk.Frame(root)
nav_frame.pack(pady=5)

btn_w = tk.Button(nav_frame, text="Maju (W)", width=10)
btn_w.grid(row=0, column=1, pady=2)
btn_a = tk.Button(nav_frame, text="Kiri (A)", width=10)
btn_a.grid(row=1, column=0, padx=2)
btn_s = tk.Button(nav_frame, text="Mundur (S)", width=10)
btn_s.grid(row=1, column=1, pady=2)
btn_d = tk.Button(nav_frame, text="Kanan (D)", width=10)
btn_d.grid(row=1, column=2, padx=2)

btn_w.bind('<ButtonPress-1>', lambda e: active_keys.add('w'))
btn_w.bind('<ButtonRelease-1>', lambda e: active_keys.discard('w'))
btn_s.bind('<ButtonPress-1>', lambda e: active_keys.add('s'))
btn_s.bind('<ButtonRelease-1>', lambda e: active_keys.discard('s'))
btn_a.bind('<ButtonPress-1>', lambda e: active_keys.add('a'))
btn_a.bind('<ButtonRelease-1>', lambda e: active_keys.discard('a'))
btn_d.bind('<ButtonPress-1>', lambda e: active_keys.discard('d'))

alt_frame = tk.Frame(root)
alt_frame.pack(pady=8)

btn_i = tk.Button(alt_frame, text="Naik (I)", width=10)
btn_i.grid(row=0, column=0, padx=5)
btn_k = tk.Button(alt_frame, text="Turun (K)", width=10)
btn_k.grid(row=0, column=1, padx=5)

btn_i.bind('<ButtonPress-1>', lambda e: active_keys.add('i'))
btn_i.bind('<ButtonRelease-1>', lambda e: active_keys.discard('i'))
btn_k.bind('<ButtonPress-1>', lambda e: active_keys.add('k'))
btn_k.bind('<ButtonRelease-1>', lambda e: active_keys.discard('k'))

btn_stop = tk.Button(root, text="Stop & Plot 3D Map", bg="red", fg="white", font=("Helvetica", 10, "bold"), command=close_app)
btn_stop.pack(pady=15, fill="x", padx=20)


def press_key(e):
    k = e.char.lower()
    if k in ['w', 'a', 's', 'd', 'i', 'k']:
        active_keys.add(k)
    elif k == 'q':
        close_app()

def release_key(e):
    k = e.char.lower()
    if k in active_keys:
        active_keys.discard(k)

root.bind('<KeyPress>', press_key)
root.bind('<KeyRelease>', release_key)
root.mainloop()

try:
    if sim.getSimulationState() != sim.simulation_stopped:
        sim.stopSimulation()
except Exception:
    pass

# PLOTTING & SAVE GAMBAR
pts = np.array(pts_data)
traj = np.array(trajectory)

print(f"\nPemindaian selesai. Total titik point cloud: {len(pts)}, Titik trajektori: {len(traj)}")

if len(pts) > 0:
    voxel_sz = 0.03
    vox = np.floor(pts / voxel_sz).astype(int)
    _, idx = np.unique(vox, axis=0, return_index=True)
    clean_pts = pts[idx]

    z_vals = clean_pts[:, 2]
    norm = plt.Normalize(np.min(z_vals), np.max(z_vals) + 1e-6)
    cmap = plt.colormaps['turbo']
    colors = cmap(norm(z_vals))[:, :3]

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("3D Mapping Result & Flight Trajectory")

    sc = ax.scatter(clean_pts[:, 0], clean_pts[:, 1], clean_pts[:, 2], c=colors, s=5, alpha=0.8)
    
    if len(traj) > 0:
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], color='red', linewidth=2, label="Trajectory")

    map_cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    map_cbar.set_array(z_vals)
    cb = fig.colorbar(map_cbar, ax=ax, shrink=0.6, pad=0.08)
    cb.set_label('Height Z (m)', rotation=270, labelpad=12)

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.legend()

    # Simpan Gambar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(script_dir, "3d_map_result.png")
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    print(f"[SUCCESS] File gambar berhasil disimpan di: {out_file}")

    plt.show()
else:
    print("[ERROR] Point cloud data tetap kosong!")
    print("PASTIKAN script Lua di 'fast3DLaserScanner' memiliki baris berikut pada sysCall_sensing():")
    print("--------------------------------------------------------------------------------")
    print('  local packedData = sim.packFloatTable(measuredData)')
    print('  sim.setBufferSignal("fast3D_data", packedData)')
    print("--------------------------------------------------------------------------------")