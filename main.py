from kivy.core.text import LabelBase
LabelBase.register(name='Korean', fn_regular='C:/코딩 피피티/pyton/fonts/NotoSansKR-VariableFont_wght.ttf')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.image import AsyncImage
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.modalview import ModalView
from datetime import datetime
import calendar
import os
import uuid
import requests
from firebase_admin import credentials, initialize_app, storage

# Firebase
cred = credentials.Certificate('firebase_key.json')
initialize_app(cred, {'storageBucket': 'saddasd-81a76.firebasestorage.app'})

user_data = {"name": ""}
if os.path.exists("username.txt"):
    with open("username.txt", "r", encoding="utf-8") as f:
        user_data["name"] = f.read().strip()

FIREBASE_URL = 'https://saddasd-81a76-default-rtdb.firebaseio.com/posts_by_date.json'
posts_by_date = {}

def upload_image_to_firebase(local_path):
    bucket = storage.bucket()
    ext = os.path.splitext(local_path)[1]
    blob = bucket.blob(f"images/{uuid.uuid4()}{ext}")
    blob.upload_from_filename(local_path)
    return f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{blob.name.replace('/', '%2F')}?alt=media"

class NameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Label(font_name='Korean', text="이름을 입력하세요", font_size=22))
        self.name_input = TextInput(font_name='Korean', hint_text="이름", multiline=False, font_size=20)
        layout.add_widget(self.name_input)
        confirm_btn = Button(font_name='Korean', text="확인", size_hint=(1, 0.3), font_size=20)
        confirm_btn.bind(on_release=self.save_name)
        layout.add_widget(confirm_btn)
        self.add_widget(layout)

    def save_name(self, instance):
        user_data["name"] = self.name_input.text.strip()
        with open("username.txt", "w", encoding="utf-8") as f:
            f.write(user_data["name"])
        if user_data["name"]:
            self.manager.current = "calendar"

class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        self.uploaded_image_url = None
        super().__init__(**kwargs)
        self.current_year = datetime.today().year
        self.current_month = datetime.today().month
        self.selected_day = None

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        header = BoxLayout(size_hint=(1, 0.1), spacing=5)
        prev_btn = Button(font_name='Korean', text='<', size_hint_x=0.1)
        next_btn = Button(font_name='Korean', text='>', size_hint_x=0.1)
        self.month_label = Label(font_name='Korean', font_size=20, size_hint_x=0.6, halign='center', valign='middle')
        name_reset_btn = Button(text='이름 변경', font_name='Korean', size_hint_x=0.2, font_size=14)
        name_reset_btn.bind(on_release=self.reset_name)

        header.add_widget(prev_btn)
        header.add_widget(self.month_label)
        header.add_widget(next_btn)
        header.add_widget(name_reset_btn)
        prev_btn.bind(on_release=lambda x: self.change_month(-1))
        next_btn.bind(on_release=lambda x: self.change_month(1))
        layout.add_widget(header)

        self.calendar_grid = GridLayout(cols=7, spacing=5, size_hint_y=None, height=280, row_default_height=40, row_force_default=True)
        layout.add_widget(self.calendar_grid)

        self.selected_date_label = Label(font_name='Korean', font_size=18, halign='left', valign='middle', size_hint_y=None, height=30)
        self.selected_date_label.bind(size=self.selected_date_label.setter('text_size'))
        layout.add_widget(self.selected_date_label)

        self.post_box = ScrollView(size_hint=(1, 0.4))
        self.post_list = GridLayout(cols=1, size_hint_y=None, spacing=8, padding=5)
        self.post_list.bind(minimum_height=self.post_list.setter('height'))
        self.post_box.add_widget(self.post_list)
        layout.add_widget(self.post_box)

        self.input_title = TextInput(font_name='Korean', hint_text='제목 입력', multiline=False, size_hint_y=None, height=30)
        self.input_category = BoxLayout(size_hint_y=None, height=30)
        self.category = '일정'
        for idx, cat in enumerate(['일정', '수행평가', '공지']):
            cb = CheckBox(group='cat', active=(idx == 0))
            lbl = Label(text=cat, font_name='Korean')
            box = BoxLayout()
            box.add_widget(cb)
            box.add_widget(lbl)
            cb.bind(active=lambda inst, val, c=cat: self.set_category(val, c))
            self.input_category.add_widget(box)

        self.input_content = TextInput(font_name='Korean', hint_text='내용 입력', multiline=True, size_hint_y=None, height=60)
        self.submit_btn = Button(font_name='Korean', text='등록', size_hint_y=None, height=35)
        self.submit_btn.bind(on_release=self.submit_post)
        self.image_btn = Button(font_name='Korean', text='사진 첨부', size_hint_y=None, height=30)
        self.image_btn.bind(on_release=self.choose_image)

        self.input_group = BoxLayout(orientation='vertical', size_hint_y=None)
        self.input_group.add_widget(self.input_title)
        self.input_group.add_widget(self.input_category)
        self.input_group.add_widget(self.input_content)
        self.input_group.add_widget(self.image_btn)
        self.input_group.add_widget(self.submit_btn)
        self.input_group.height = 160
        layout.add_widget(self.input_group)

        bottom_bar = BoxLayout(size_hint_y=None, height=60, padding=10)
        self.add_btn = Button(text='+', font_name='Korean', size_hint=(1, 1))
        self.add_btn.bind(on_release=self.toggle_input_group)
        bottom_bar.add_widget(self.add_btn)
        layout.add_widget(bottom_bar)

        self.input_group.opacity = 0
        self.input_group.disabled = True

        self.load_from_firebase(callback=self.post_load_setup)

    def reset_name(self, instance):
        user_data["name"] = ""
        try:
            os.remove("username.txt")
        except:
            pass
        self.manager.current = "name"

    def post_load_setup(self):
        self.render_calendar()
        if self.selected_day is None:
            self.selected_day = datetime.today().day
        self.select_day(self.selected_day)
        self.start_auto_refresh()

    def start_auto_refresh(self):
        def refresh(dt):
            self.load_from_firebase()
            if self.selected_day:
                self.select_day(self.selected_day)
        Clock.schedule_interval(refresh, 10)

    def set_category(self, active, category):
        if active:
            self.category = category

    def choose_image(self, instance):
        filechooser = ModalView(size_hint=(0.9, 0.9))
        chooser = FileChooserIconView(path=os.path.expanduser('~'), filters=['*.png', '*.jpg', '*.jpeg'])

        def on_selection(*args):
            selection = chooser.selection
            if selection:
                self.selected_image_path = selection[0]
                try:
                    self.uploaded_image_url = upload_image_to_firebase(self.selected_image_path)
                except Exception as e:
                    print("이미지 업로드 실패:", e)
                    self.uploaded_image_url = None
                filechooser.dismiss()

        chooser.bind(on_submit=on_selection)
        filechooser.add_widget(chooser)
        filechooser.open()

    def submit_post(self, instance):
        if not self.selected_day:
            return
        date_key = f"{self.current_year}-{self.current_month:02}-{self.selected_day:02}"
        if not self.input_title.text.strip():
            return
        post = {
            'id': str(uuid.uuid4()),
            'title': self.input_title.text,
            'content': self.input_content.text,
            'category': self.category,
            'author': user_data['name'],
            'image_url': getattr(self, 'uploaded_image_url', None)
        }
        existing = posts_by_date.get(date_key)
        if not isinstance(existing, list):
            posts_by_date[date_key] = [post]
        else:
            posts_by_date[date_key].append(post)
        self.upload_to_firebase(date_key)
        self.input_title.text = ''
        self.input_content.text = ''
        self.uploaded_image_url = None
        self.show_inputs(False)
        self.render_calendar()
        if self.selected_day:
            self.select_day(self.selected_day)

    def upload_to_firebase(self, date_key):
        try:
            url = f"https://saddasd-81a76-default-rtdb.firebaseio.com/posts_by_date/{date_key}.json"
            requests.put(url, json=posts_by_date[date_key])
        except Exception as e:
            print("Firebase 업로드 실패:", e)

    def load_from_firebase(self, callback=None):
        try:
            response = requests.get(FIREBASE_URL)
            if response.ok:
                global posts_by_date
                posts_by_date = response.json() or {}
            if callback:
                callback()
        except Exception as e:
            print("Firebase 불러오기 실패:", e)

    def show_inputs(self, visible):
        self.input_group.opacity = 1 if visible else 0
        self.input_group.disabled = not visible

    def toggle_input_group(self, instance):
        is_visible = self.input_group.opacity == 1
        self.show_inputs(not is_visible)

    def select_day(self, day):
        self.selected_day = day
        self.selected_date_label.text = f"{self.current_month}월 {day}일 일정"
        self.post_list.clear_widgets()
        self.render_calendar()
        date_key = f"{self.current_year}-{self.current_month:02}-{day:02}"
        posts = posts_by_date.get(date_key, [])
        for post in posts:
            if isinstance(post, dict):
                preview_text = f"[{post['category']}] {post['title']} - {post['author']}"
            else:
                continue
            btn = Button(text=preview_text, font_name='Korean', size_hint_y=None, height=45, font_size=14)

            def show_popup(instance, p=post):
                layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
                layout.add_widget(Label(text=f"제목: {p['title']}", font_name='Korean'))
                layout.add_widget(Label(text=f"카테고리: {p['category']}", font_name='Korean'))
                layout.add_widget(Label(text=f"작성자: {p['author']}", font_name='Korean'))
                layout.add_widget(Label(text=f"내용: {p['content']}", font_name='Korean'))

                if p.get('image_url'):
                    try:
                        layout.add_widget(AsyncImage(source=p['image_url'], size_hint_y=None, height=150))
                    except Exception as e:
                        print("이미지 로딩 실패:", e)

                btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
                close_btn = Button(text='닫기', font_name='Korean')
                btn_box.add_widget(close_btn)

                if p['author'] == user_data['name']:
                    delete_btn = Button(text='삭제', font_name='Korean')

                    def delete_post(btn_instance):
                        if date_key in posts_by_date:
                            posts_by_date[date_key] = [item for item in posts_by_date[date_key] if item.get('id') != p.get('id')]
                            try:
                                url = f"https://saddasd-81a76-default-rtdb.firebaseio.com/posts_by_date/{date_key}.json"
                                requests.put(url, json=posts_by_date[date_key])
                            except Exception as e:
                                print("Firebase 삭제 동기화 실패:", e)
                        popup.dismiss()
                        self.select_day(self.selected_day)

                    delete_btn.bind(on_release=delete_post)
                    btn_box.add_widget(delete_btn)

                layout.add_widget(btn_box)
                popup = Popup(title='일정 상세 보기', content=layout, size_hint=(0.8, 0.6))
                close_btn.bind(on_release=popup.dismiss)
                popup.open()

            btn.bind(on_release=show_popup)
            self.post_list.add_widget(btn)

    def render_calendar(self):
        self.calendar_grid.clear_widgets()
        self.month_label.text = f'{self.current_year}년 {self.current_month}월'

        days = ['일', '월', '화', '수', '목', '금', '토']
        for day in days:
            self.calendar_grid.add_widget(Label(text=day, bold=True, font_name='Korean'))

        cal = calendar.Calendar(firstweekday=6)
        for day in cal.itermonthdays(self.current_year, self.current_month):
            if day == 0:
                self.calendar_grid.add_widget(Label(text=''))
            else:
                date_key = f"{self.current_year}-{self.current_month:02}-{day:02}"
                has_post = date_key in posts_by_date and posts_by_date[date_key]
                day_label = str(day)
                if has_post:
                    day_label += ' [color=#FF0000]•[/color]'
                btn = Button(text=day_label, font_name='Korean', markup=True, size_hint_y=None, height=40, background_normal='', background_color=(0.2, 0.2, 0.2, 1))
                if has_post:
                    day_label += ' [color=#FF0000]•[/color]'  # 빨간 점을 의미하는 유니코드 문자  # 일정 있는 날 강조 색상
                if self.is_today(day):
                    btn.color = (1, 0, 0, 1)
                    if self.selected_day is None:
                        self.selected_day = day
                if self.selected_day and day == self.selected_day:
                    btn.background_color = (1, 0, 0, 0.3)
                btn.bind(on_release=lambda inst, d=day: self.select_day(d))
                self.calendar_grid.add_widget(btn)

    def change_month(self, offset):
        self.current_month += offset
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.render_calendar()

    def is_today(self, day):
        today = datetime.today()
        return self.current_year == today.year and self.current_month == today.month and day == today.day

class ClassScheduleApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(NameScreen(name='name'))
        sm.add_widget(CalendarScreen(name='calendar'))

        if user_data["name"]:
            sm.current = 'calendar'
        else:
            sm.current = 'name'

        return sm

if __name__ == '__main__':
    ClassScheduleApp().run()
