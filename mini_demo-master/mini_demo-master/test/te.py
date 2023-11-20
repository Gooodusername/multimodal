import asyncio

from mini.apis import errors
from mini.apis.api_sound import ChangeRobotVolume, ChangeRobotVolumeResponse
from mini.apis.api_sound import FetchAudioList, GetAudioListResponse, AudioSearchType
from mini.apis.api_sound import PlayAudio, PlayAudioResponse, AudioStorageType
# from mini.apis.api_sound import PlayOnlineMusic, MusicResponse
from mini.apis.api_sound import StartPlayTTS, StopPlayTTS, ControlTTSResponse
from mini.apis.api_sound import StopAllAudio, StopAudioResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program
from mini.apis.api_action import PlayAction, PlayActionResponse

async def main():
    device: WiFiDevice = await test_get_device_by_name()
    await test_connect(device)
    await test_start_run_program()
    b=StartPlayTTS(text="亲爱的领导们，让我给你跳支舞吧。")
    # b=StartPlayTTS(text="鸡你太美 baby 鸡你太美 baby 鸡你实在是太美 baby 鸡你太美 baby 迎面走来的你让我如此蠢蠢欲动,这种感觉我从未有,Cause I got a crush on you who you,你是我的我是你的谁再多一眼看一眼就会爆炸,再近一点靠近点快被融化")
    # await b.execute()
    # time.sleep(5)
    a:PlayAction=PlayAction(action_name="dance_0002")
    await a.execute()

    # a:PlayAction=PlayAction(action_name="009")
    # await a.execute()

    # a:PlayAction=PlayAction(action_name="028")
    # await a.execute()

    await MiniSdk.quit_program()
    await MiniSdk.release()

asyncio.run(main())



