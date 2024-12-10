# 在 0.9.13、0.9.15 中进行了测试
# 参考： https://github.com/PJLab-ADG/PCSim/blob/0a0ea957f489ef14c4db338f0c035bd41f0544f1/ReSimAD/src/walker_control.py
import random

import carla


class BaseWalkerPose:
    def control(self, walker, left_roll=None, right_roll=None):
        bones = walker.get_bones().bone_transforms  # 获得行人的骨架
        TR = bones[56].relative
        TL = bones[61].relative
        AR = bones[5].relative
        AL = bones[33].relative
        if left_roll is None or right_roll is None:
            total = random.randint(0, 40)
            left_roll = random.randint(0, total)
            right_roll = total + total - left_roll

        thigh_r = ('crl_thigh__R', carla.Transform(location=TR.location,
                                                   rotation=carla.Rotation(roll=TR.rotation.roll + right_roll,
                                                                           yaw=TR.rotation.yaw,
                                                                           pitch=TR.rotation.pitch)))
        thigh_l = ('crl_thigh__L', carla.Transform(location=TL.location,
                                                   rotation=carla.Rotation(roll=TL.rotation.roll - left_roll,
                                                                           yaw=TL.rotation.yaw,
                                                                           pitch=TL.rotation.pitch)))
        arm_r = ('crl_arm__R', carla.Transform(location=AR.location,
                                               rotation=carla.Rotation(
                                                   roll=AR.rotation.roll,
                                                   yaw=AR.rotation.yaw,
                                                   pitch=AR.rotation.pitch + left_roll * 0.8)))
        arm_l = ('crl_arm__L', carla.Transform(location=AL.location,
                                               rotation=carla.Rotation(
                                                   roll=AL.rotation.roll,
                                                   yaw=AL.rotation.yaw,
                                                   pitch=AL.rotation.pitch + right_roll * 0.8)))
        control = carla.WalkerBoneControlIn([thigh_r, thigh_l, arm_l, arm_r])
        control.bone_transforms = [thigh_r, thigh_l, arm_l, arm_r]
        walker.blend_pose(1)
        walker.set_bones(control)
        walker.show_pose()

    def demo(self):
        client = carla.Client('127.0.0.1', 2000)
        world = client.get_world()
        blueprint = random.choice(world.get_blueprint_library().filter('walker.*'))
        # z小于报错：AttributeError: 'NoneType' object has no attribute 'set_simulate_physics'
        spawn_point = carla.Transform(carla.Location(0, 5, 1), carla.Rotation(0, 0, 0))
        walker = world.try_spawn_actor(blueprint, spawn_point)
        walker.set_simulate_physics(False)

        # 将相机转向行人的生成点
        trans = walker.get_transform()
        spectator = world.get_spectator()
        spectator.set_transform(trans)

        self.control(walker, 35, 35)


wp = BaseWalkerPose()
wp.demo()
