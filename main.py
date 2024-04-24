import os
import re

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage

yaml_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        user = await self.api.me()
        _log.info(user)
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    @staticmethod
    async def on_group_at_message_create(message: GroupMessage):
        if re.match(r"\s*/test", message.content.strip()):
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content="test123")
        if re.match(r"\s*/loli", message.content.strip()):
            # 上传图片文件
            upload_media = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,  # 文件类型为图片
                url="https://api.xiwangly.top/image.php?key=xiwangly"
            )
            # 发送消息，带上上传的图片作为媒体
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,  # 富媒体类型
                msg_id=message.id,
                content="你要的萝莉：",
                media=upload_media
            )
        message_result = await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=f"收到了消息：「{message.content.strip()}」")
        _log.info(message_result)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    intents = botpy.Intents.none()
    intents.public_messages = True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=yaml_config["appid"], secret=yaml_config["secret"])
