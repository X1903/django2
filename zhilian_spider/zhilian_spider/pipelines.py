# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
from scrapy.conf import settings


class ZhilianSpiderPipeline(object):

    def process_item(self, item, spider):
        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']

        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c)
        cur = con.cursor()

        sql = "INSERT INTO zhilian" \
              "(job_id, job_name, job_company, job_salary, job_education, job_address, job_category, job_description, company_profile) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        if item['job_name']:
            list = [item['job_id'], item['job_name'], item['job_company'], item['job_salary'], item['job_education'],
                    item['job_address'],
                    item['job_category'], item['job_description'], item['company_profile']]

            try:
                cur.execute(sql, list)

            except Exception as e:
                print('Insert error', e)
                con.rollback()

            else:
                con.commit()
                cur.close()
                con.close()

        return item

