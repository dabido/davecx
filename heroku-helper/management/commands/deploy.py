from django.core.management.base import BaseCommand, make_option
from optparse import make_option
from davecx.settings import MANAGE_DIR, HEROKU_APP, HEROKU_API_KEY
import heroku
import os
import inspect

class Command(BaseCommand):
	help = 'Deploys app to Heroku'

	option_list = BaseCommand.option_list + (
		make_option('--maintenance',
			action='store_true',
			dest='maintenance',
			default=False,
			help='Activate maintenance mode before deploying'
		),

		make_option('--bump_assets',
			action='store_true',
			dest='bump_assets',
			default=False,
			help='Bump all assets to bust cache'
		),

		make_option('--collect_static',
			action='store_true',
			dest='collect_static',
			default=False,
			help='Collect staticfiles after deploy'
		),

		make_option('--flush_cache',
			action='store_true',
			dest='flush_cache',
			default=False,
			help='Collect staticfiles after deploy'
		),

		make_option('--use_all',
			action='store_true',
			dest='use_all',
			default=False,
			help='Combines maintenance, bump_assets and collect_static'
		),
	)

	def handle(self, *args, **options):
		use_maintenance = options['maintenance']
		bump_assets = options['bump_assets']
		collect_static = options['collect_static']
		use_all = options['use_all']
		flush_cache = options['flush_cache']

		print "All right, deploying your shit now"
		os.chdir(MANAGE_DIR)

		if use_maintenance or use_all:
			os.system("heroku maintenance:on")

		# Deploy to heroku
		print "\nDeploying to heroku..."
		os.system("git push heroku master")

		if collect_static or use_all:
			print "\nCollecting all staticfiles..."
			os.system("heroku run python manage.py collectstatic --noinput")

		if bump_assets or use_all:
			print "\nUpdating asset version"
			cloud = heroku.from_key(HEROKU_API_KEY)
			app = cloud.apps[HEROKU_APP]
			last_release = app.releases[-1]

			app.config['APP_REVISION'] = last_release.name

		if flush_cache or use_all:
			print "\nFlushing memcache..."
			cmd = ('''heroku run "python -c \\"'''
					'''import os;'''
					'''os.environ['DJANGO_SETTINGS_MODULE'] = 'davecx.settings';'''
					'''from django.core.cache import cache;'''
					'''cache.clear();'''
					'''\\" " ''') # Closing quotes for 'heroku run' and 'python -c'

			os.system(cmd)

		if use_maintenance or use_all:
			os.system("heroku maintenance:off")