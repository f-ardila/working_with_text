import os


start_date = '20170101'
# start_date = '20200101'
end_date = '20200701'
# end_date = '20200201'
tag = 'wellness'
output_dir = 'scraped_data/'
output_file = output_dir+start_date+tag+end_date+'.json'
scrapper_file = 'medium_scraper_tag_archive.py'
log_file = 'logs/'+start_date+tag+end_date+'.log'

if os.path.exists(output_file):
    os.remove(output_file)

os.system('scrapy runspider -a tag={tag} -a start_date={start_date} -a end_date={end_date} --logfile {log_file} {scrapper_file} -o {output_file}'.format(tag=tag,start_date=start_date,end_date=end_date,scrapper_file=scrapper_file,output_file=output_file, log_file = log_file))
