@dataclass

class SpiderRewardCfg:
    allow_jump: bool
    w_vel: bool
    w_yaw: float
    w_upright: float
    w_alive: float
    w_act: float
    w_smooth: float
    w_slip: float
    w_vz_pen: float
    w_airtime_pen: float

    min_height: float
    max_tilt_deg: float

FAT 
