import os
from crawler import InsCrawler
import argparse
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testgraphene.settings")

import re

re_hastag = re.compile(r"#([0-9A-Za-zá-úÁ-Ú]+)", re.UNICODE)

def transform_ins_to_num(ins_string):
    if 'k' in ins_string:
        return int(float(ins_string.replace('k', '').replace(',', '.')) * 1000)
    if 'm'in ins_string:
        return int(float(ins_string.replace('m', '').replace(',', '.')) * 1000000)
    else:
        return int(ins_string.replace('.', '').replace(',', ''))



def insert_post(social_user_object, photo):
    from crawler.models import Post
    try:
        Post.objects.create(
            content=photo['content'],
            img_url=photo['img_url'],
            hashtags=" ".join(re_hastag.findall(photo['content'])).lower(),
            likes_num=transform_ins_to_num(photo['likes']),
            comments_num=transform_ins_to_num(photo['comments']),
            user=social_user_object
        )
    except:
        post = Post.objects.get(img_url=photo['img_url'])
        post.likes_num=transform_ins_to_num(photo['likes'])
        post.comments_num=transform_ins_to_num(photo['comments'])
        post.save()



def get_posts(tag, number, url=None):
    from crawler.models import SocialUser


    ins_crawler = InsCrawler()
    ins_crawler.login()
    if url is None:
        url = '%s/explore/tags/%s/' % (InsCrawler.URL, tag)
    ins_crawler.browser.get(url)
    posts = ins_crawler._get_posts(number)
    users = []
    for photo in posts:
        try:
            username = ins_crawler.get_user_profile_from_photo(photo['photo_url'])
            user_data = ins_crawler.get_user_profile(username)
            user_data['follower_num'] = transform_ins_to_num(user_data['follower_num'])
            user_data['following_num'] = transform_ins_to_num(user_data['following_num'])
            user_data['post_num'] = transform_ins_to_num(user_data['post_num'])
            try:
                social_user_object = SocialUser.objects.create(username=username,
                                                               name=user_data['name'],
                                                               photo_url=user_data['photo_url'],
                                                               post_num=user_data['post_num'],
                                                               follower_num=user_data['follower_num'],
                                                               following_num=user_data['following_num'])
            except:
                social_user_object = SocialUser.objects.get(username=username)
                social_user_object.name = user_data['name']
                social_user_object.photo_url = user_data['photo_url']
                social_user_object.post_num = user_data['post_num']
                social_user_object.follower_num = user_data['follower_num']
                social_user_object.following_num = user_data['following_num']
                social_user_object.save()

            insert_post(social_user_object, photo)
            posts_user = ins_crawler._get_posts(6)
            for post_user in posts_user:
                insert_post(social_user_object, post_user)
        except:
            pass



if __name__ == '__main__':
    django.setup()
    parser = argparse.ArgumentParser(description='Instagram Crawler')
    parser.add_argument('-t', '--tag', help='instagram\'s tag name')
    parser.add_argument('-u', '--url', help='instagram\'s searcher url')
    args = parser.parse_args()
    get_posts(args.tag, 10, args.url or None)
