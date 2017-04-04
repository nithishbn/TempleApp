import sqlite3
import datetime
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView


class LoginScreen(Screen):
    screenlist = ListProperty([])

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.screenlist.append("LoginScreen")

    def register(self):
        self.manager.current = "RegisterScreen"

    def on_enter(self, *args):
        print("Login")


class RegisterScreen(Screen):
    pass


class MenuScreen(Screen):
    screenlist = ListProperty([])

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.screenlist.append("MenuScreen")
        print(self.screenlist)

    def on_enter(self):
        super(MenuScreen, self).on_enter()
        # if self.manager.current not in self.screenlist:
        #     self.screenlist.append(self.manager.current)
        # print("Menu", self.screenlist)
        self.ids.scrolllabelthing.update_self()


class DateScreen(Screen):
    date = StringProperty('')
    otherdate = StringProperty('')
    screenlist = ListProperty([])

    def __init__(self, **kwargs):
        super(DateScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.onBackBtn)

    # def on_enter(self, *args):
    #     super(DateScreen, self).on_enter()
    #     screenlist = self.screenlist
    #     if self.manager.current not in self.screenlist:
    #         self.screenlist.append(self.manager.current)
    #     print("DateScreen", self.screenlist)
    #     # print(self.screenlist)
    def onBackBtn(self, window, key, *args):
        if key == 27:
            print(self.screenlist)
            if len(self.screenlist) != 0:
                self.manager.current = self.screenlist[len(self.screenlist) - 1]
                self.screenlist.pop(len(self.screenlist) - 1 )
                return True
            else:
                return False

    def selectdate(self):
        self.date = self.ids.datething.text
        self.screenlist.append(self.manager.current)
        self.manager.current = "TodayScreen"

    def figuretime(self):
        dt = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
        actualdate = '{0}/{1}/{2:02}'.format(dt.month, dt.day, dt.year % 100)
        return actualdate


class ConstructionScreen(Screen):
    screenlist = ListProperty([])


class TodayScreen(Screen):
    screenlist = ListProperty([])
    samva = StringProperty('')
    avanam = StringProperty('')
    rithu = StringProperty('')
    maasae = StringProperty('')
    pakshae = StringProperty('')
    thithi = StringProperty('')
    date = StringProperty('')
    screenlist = ListProperty([])

    # def __init__(self, **kwargs):
    #     super(TodayScreen, self).__init__(**kwargs)
    #     Window.bind(on_keyboard=self.onBackBtn)

    def search(self):
        date = self.date
        print(date)
        conn = sqlite3.connect('calendar.sqlite')
        cur = conn.cursor()
        try:
            cur.execute(
                '''SELECT date, S.Name, A.Name, R.Name, M.Name, P.Name, V.Name, T.Name FROM Main JOIN Samvatsaram S on Main.samvatsaram = S.SID JOIN Ayanam A on Main.ayanam = A.AID JOIN Rithu R on Main.rithu = R.RID JOIN Maasae M on Main.maasa = M.MID JOIN Pakshae P on Main.pakshae = P.PID JOIN Vaaram V on Main.Vaaram = V.VID JOIN Thithi T on Main.thithi = T.TID WHERE date = ?''',
                (date,))
            thing = cur.fetchone()
            for query in thing:
                if query == thing[0]:
                    print("Date:", query)
                elif query == thing[1]:
                    print("Samvatsaramam:", query)
                    self.samva = query
                elif query == thing[2]:
                    print("Ayanam:", query)
                    self.avanam = query
                elif query == thing[3]:
                    print("Rithu:", query)
                    self.rithu = query
                elif query == thing[4]:
                    print("Maasae:", query)
                    self.maasae = query
                elif query == thing[5]:
                    print("Pakshae:", query)
                    self.pakshae = query
                elif query == thing[6]:
                    print("Day:", query)
                elif query == thing[7]:
                    print("Thithi:", query)
                    self.thithi = query
        except:
            self.manager.current = "DateScreen"
            # self.ids.datething.text = " "


class ScrollLabel(ScrollView):
    def __init__(self, **kwargs):

        super(ScrollLabel, self).__init__(**kwargs)
        Clock.schedule_once(self.update_self)
        Clock.schedule_interval(self.update_self, 2.5)

    def update_self(self, *args):
        if self.scroll_x == 0:
            marquee = Animation(scroll_x=1.0, duration=10.0)
            marquee.start(self)
        elif self.scroll_x >= 0.99:
            self.scroll_x = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return 0


class ScreenManager(ScreenManager):
    pass


class InterfaceApp(App):
    def on_pause(self):
	return True


InterfaceApp().run()
