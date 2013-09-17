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

		os.chdir(MANAGE_DIR)

		if use_maintenance or use_all:
			os.system("heroku maintenance:on")

		# Deploy to heroku
		os.system("git push heroku master")

		if collect_static or use_all:
			os.system("heroku run python manage.py collectstatic --noinput")

		if bump_assets or use_all:
			cloud = heroku.from_key(HEROKU_API_KEY)
			app = cloud.apps[HEROKU_APP]
			last_release = app.releases[-1]

			app.config['ASSET_VERSION'] = last_release.name

		if use_maintenance or use_all:
			os.system("heroku maintenance:off")