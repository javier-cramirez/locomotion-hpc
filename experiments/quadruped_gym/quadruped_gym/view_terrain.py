import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("terrain.xml")
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    # just idle the sim so you can orbit/zoom
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
