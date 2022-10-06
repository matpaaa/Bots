from .Logger         import Log
from .AddCog         import AddCog
from .GetLang        import Get_Lang

from .type.Interface import Interface as _Interface
from .type.Options   import Options   as _Options
from .Statu          import Status    as _Status

from .Utils          import Open, MISSING

from time            import sleep

import os, asyncio
import threading

try:
    import discord
    from discord.ext import commands
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'discord'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)


class Bot(threading.Thread):
    _initialized: bool = False
    _error      : bool = False

    def __init__(self, Id: str = MISSING, Options: _Options = MISSING) -> None:
        super(Bot, self).__init__()

        if Id == MISSING:
            Log(50, Get_Lang.get('0.0.1.4.9').format(Error = Get_Lang.get('0.0.1.5.0')))
            self._error = True
            return

        elif Options == MISSING:
            Log(50, Get_Lang.get('0.0.1.4.9').format(Error = Get_Lang.get('0.0.1.5.1')))
            self._error = True
            return

        self._event: int            = 0
        self._interface: _Interface = None

        self._id: str               = Id
        self._options: _Options     = Options

        self._status: _Status       = _Status(self, self._options)

        if not os.path.exists('{0}/User/Bots/{1}/'.format(self._options.Path, self._id)):
            os.makedirs('{0}/User/Bots/{1}/'.format(self._options.Path, self._id), exist_ok = True)

        self._prefix: dict          = Open('{0}/User/Bots/{1}/Prefix.json'.format(self._options.Path, self._id), {'Prefix': ["!"]})
        self._info: dict            = Open('{0}/User/Bots/{1}/Main.json'.format(self._options.Path, self._id))

        self._status_: str          = '0.0.0.6.2'
        self._client: commands.Bot  = None
        self._ping: float           = 0.0

        self._initialized: bool     = True

    def run(self) -> None:
        while True:
            if self._event == 0:
                sleep(0.5)
            elif self._event == 1:
                self._event = 0
                asyncio.run(self._Start())

    async def _Start(self) -> None:
        if not self._initialized:
            return

        if not self.Info.get('Token', False):
            Log(30, Get_Lang.get('0.0.0.1.3'))
            return

        try:
            self.Client = commands.Bot((self._prefix_), intents = discord.Intents.all())
        except discord.errors.PrivilegedIntentsRequired:
            self.Client = commands.Bot((self._prefix_))

        if not await AddCog(self):
            Log(30, 'Les modules n\'ont pas reussi a etre ajouter')
        self.Status.Start()

        try:
            await self.Client.start(self.Info.get('Token'))
        except KeyboardInterrupt:
            Log(50, Get_Lang.get('0.0.1.4.6'))
            self.Client.loop.create_task(self.Client.close())
        except Exception as e:
            Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

    def _prefix_(self, client: commands.Bot, message: discord.Message) -> list:
        _prefix: list = []

        for prefix in self.Prefix.get('Prefix', []):
            _prefix.append(prefix)

        if message.guild:
            if not os.path.exists('{0}/User/{1}/__Guilds__/{2}/'.format(self._options.Path, client.user.id, message.guild.id)):
                os.makedirs('{0}/User/{1}/__Guilds__/{2}/'.format(self._options.Path, client.user.id, message.guild.id), exist_ok = True)

            guild_prefix: dict = Open('{0}/User/{1}/__Guilds__/{2}/Main.json'.format(self._options.Path, client.user.id, message.guild.id), {'Prefix': []})
            for prefix in guild_prefix:
                _prefix.append(prefix)

        return _prefix

    def Stop(self) -> bool:
        if self.Status == '0.0.0.6.2':
            return False

        if self.Client == None:
            return False

        self._status.Stop()
        try:
            self.Client.loop.create_task(self.Client.close())
        except Exception:
            return False
        
        else:
            self.Status_ = '0.0.0.6.2'
            self.Interface.UpDate_Bot(self.Id)
            self.Client = None

            return True

    def Start(self) -> bool:
        try:
            self._event = 1
        except Exception:
            return False
        
        else:
            return True

    @property
    def Initialized(self) -> bool:
        return self._initialized

    @property
    def Error(self) -> bool:
        return self._error

    @property
    def Interface(self) -> _Interface:
        return self._interface

    @Interface.setter
    def Interface(self, value: _Interface = MISSING) -> _Interface:
        if value:
            self._interface = value

        return self._interface

    @property
    def Id(self) -> str:
        return self._id

    @Id.setter
    def Id(self, value: str = MISSING) -> str:
        if value:
            self._id = value

        return self._id

    @property
    def Options(self) -> _Options:
        return self._options

    @Options.setter
    def Options(self, value: _Options = MISSING) -> _Options:
        if value:
            self._options = value

        return self._options

    @property
    def Status(self) -> _Status:
        return self._status

    @Status.setter
    def Status(self, value: _Status = MISSING) -> _Status:
        if value:
            self._status = value

        return self._status

    @property
    def Prefix(self) -> dict:
        return self._prefix

    @Prefix.setter
    def Prefix(self, value: dict = MISSING) -> dict:
        if value:
            self._prefix = value

        return self._prefix

    @property
    def Info(self) -> dict:
        return self._info

    @Info.setter
    def Info(self, value: dict = MISSING) -> dict:
        if value:
            self._info = value

        return self._info

    @property
    def Status_(self) -> str:
        return self._status_

    @Status_.setter
    def Status_(self, value: str = MISSING) -> str:
        if value:
            self._status_ = value

        return self._status_

    @property
    def Client(self) -> commands.Bot:
        return self._client

    @Client.setter
    def Client(self, value: commands.Bot = MISSING) -> commands.Bot:
        if value:
            self._client = value

        return self._client

    @property
    def Ping(self) -> float:
        return self._ping

    @Ping.setter
    def Ping(self, value: float = MISSING) -> float:
        if value:
            self._ping = value

        return self._ping