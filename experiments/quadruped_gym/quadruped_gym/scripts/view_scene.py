import mujoco
import mujoco.viewer

XML = "fat_spider.xml"  # the patched XML in scene/

model = mujoco.MjModel.from_xml_path(XML)
data  = mujoco.MjData(model)

# optional: step a bit so it settles
for _ in range(10):
    mujoco.mj_step(model, data)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()

