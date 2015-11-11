# -*- coding:utf-8 -*-
import sublime, sublime_plugin
import sys
import threading
import json
import urllib


class Constants: 
	SETTINGS_FILE = 'Codic.sublime-settings'

def defailt_s(str):
	if str is None:
		return ''
	return str

class CodicAPI(object):
	def __init__(self, access_token):
		self.host = "https://api.codic.jp"
		self.access_token = access_token

	def get_user_projects(self, callback, context):
		uri = self.host+"/v1/user_projects.json"
		thread = threading.Thread(target=self, args=(uri, callback, context))
		thread.setDaemon(True)
		thread.start()

	def translate(self, project_id, source_text, options, callback, context):
		uri = self.host+"/v1/engine/translate.json?"+ urllib.parse.urlencode({'text':defailt_s(source_text), 'project_id':defailt_s(project_id), 'casing': options['letter_case'] })
		thread = threading.Thread(target=self, args=(uri, callback, context))
		thread.setDaemon(True)
		thread.start()

	def __call__(self, uri, callback, context):
		(status, result) = self._get(uri)
		callback(status, result, context)

	def _get(self, uri):
		headers = { 'Authorization': 'Bearer '+self.access_token }
		req = urllib.request.Request(uri, None, headers)
		try:
			response = urllib.request.urlopen(req)
			return (200, json.loads(response.read().decode("utf-8")))
		except urllib.request.HTTPError as e:
			return (e.code, json.loads(e.read().decode("utf-8")))

class SelectProjectCommand(sublime_plugin.ApplicationCommand):
	def __init__(self, *args, **kwargs):
		sublime_plugin.ApplicationCommand.__init__(self, *args, **kwargs)

	def description(self, args):
		return "Select Project"

	def run(self):
		settings = sublime.load_settings(Constants.SETTINGS_FILE)
		access_token = settings.get('access_token')
		if access_token is None:
			return

		api = CodicAPI(access_token)
		api.get_user_projects(self.on_load, {})

	def on_load(self, status, result, context):
		if status != 200:
			sublime.set_timeout(lambda: sublime.error_message(u'Failed to call API, due to : '+result['errors'][0]['message']), 1)
			return

		settings = sublime.load_settings(Constants.SETTINGS_FILE)
		current = settings.get("project_id")

		selections = [ '(System dictionary)' ] + list(map(lambda t:t.get('name'), result))
		self.candidates = [ None ] + list(map(lambda t:t.get('id'), result))
		try:
			selected = self.candidates.index(current)
		except ValueError as e:
			selected = 0
			pass
		sublime.set_timeout(lambda: sublime.active_window().show_quick_panel(selections, self.on_select, 0, selected), 1)

	def on_select(self, index):
		if index == -1:
			return

		settings = sublime.load_settings(Constants.SETTINGS_FILE)
		settings.set("project_id", self.candidates[index])
		sublime.save_settings(Constants.SETTINGS_FILE)
		sublime.set_timeout(lambda: sublime.error_message(u'Successfully updated.'), 1)

class ChangeLetterCaseCommand(sublime_plugin.ApplicationCommand):
	def __init__(self, *args, **kwargs):
		sublime_plugin.ApplicationCommand.__init__(self, *args, **kwargs)
		self.candidates = []
		self.candidatesValues = []
		self.selections = [ '[Aa] PascalCase', '[aA] camelCase', '[a_a] Lower underscore', '[A_A] Upper underscore', '[a-a] Hyphenation', '[a a] None' ]
		self.ids =        [ 'pascal', 'camel', 'lower underscore', 'upper underscore', 'hyphen', '' ]

	def run(self):
		settings = sublime.load_settings(Constants.SETTINGS_FILE)
		selected = 0
		try:
			selected = self.ids.index(settings.get("letter_case"))
		except ValueError as e:
			selected = 0
			pass

		sublime.set_timeout(lambda: sublime.active_window().show_quick_panel(self.selections, self.on_select, 0, selected), 1)

	def on_select(self, index):
		if index == -1:
			return

		settings = sublime.load_settings(Constants.SETTINGS_FILE)
		settings.set("letter_case", self.ids[index])
		sublime.save_settings(Constants.SETTINGS_FILE)

class SetAccessTokenCommand(sublime_plugin.ApplicationCommand):
	def __init__(self, *args, **kwargs):
		sublime_plugin.ApplicationCommand.__init__(self, *args, **kwargs)
		self.candidates = []
		self.candidatesValues = []

	def run(self):
		settings = sublime.load_settings(Constants.SETTINGS_FILE)
		access_token = settings.get('access_token')
		if access_token is None:
			access_token = ''
		sublime.active_window().show_input_panel('Access token : ', access_token, self.on_input, None, None)

	def on_input(self, result):
		settings = sublime.load_settings(Constants.SETTINGS_FILE)
		settings.set("access_token", result)
		sublime.save_settings(Constants.SETTINGS_FILE)
		sublime.set_timeout(lambda: sublime.error_message(u'Successfully updated.'), 1)

class GenerateNamingCommand(sublime_plugin.TextCommand):
	def __init__(self, *args, **kwargs):
		sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
		self.candidates = []
		self.settings = sublime.load_settings(Constants.SETTINGS_FILE)

	def run(self, edit):
		text = None
		for region in self.view.sel():
			if not region.empty():
				text = self.view.substr(region)

		if text is None or text == '':
			sublime.active_window().show_input_panel('Text to generate [ja]', '', lambda text_: self.on_input(text_, edit), None, None)
			return

		self.on_input(text, edit)

	def on_input(self, text, edit):
		if text is None or text == '':
			return

		access_token = self.settings.get('access_token')
		if (access_token is None):
			sublime.set_timeout(lambda: sublime.error_message(u"Access token required."), 1)
			return

		project_id = self.settings.get('project_id')
		letter_case = self.settings.get('letter_case')
		api = CodicAPI(access_token)

		# TODO : Supports multi-line text and multi selection.
		api.translate(project_id, text, {'letter_case': letter_case}, self.on_load, {'edit':edit})

	def on_load(self, status, result, context):
		if status != 200:
			sublime.set_timeout(lambda: sublime.error_message(u'Failed to call API, due to : '+result['errors'][0]['message']), 1)
			return

		if len(result[0]['words']) == 1 and result[0]['words'][0]['successful']:
			self.candidates = list(map(lambda t:t.get('text'), result[0].get('words')[0].get('candidates')))
		else:
			self.candidates = [ result[0].get('translated_text') ]	

		view = sublime.active_window().active_view()
		view.show_popup_menu(self.candidates, lambda i:self.on_select(i, context))

	def on_select(self, index, context):
		if index == -1:
			return

		text_to_replace = self.candidates[index];
		
		#sublime.set_timeout(lambda: self.view.insert(context['edit'], 0, text_to_replace), 1)
		#for region in self.view.sel():
		#	if not region.empty():
		self.view.run_command("insert", {"characters": text_to_replace})





