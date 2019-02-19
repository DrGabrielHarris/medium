from datetime import datetime
import pandas as pd
import calendar
import facebook
import json


class PageApp(object):
    def __init__(self, json_file_name, version):
        super().__init__()

        # open json file to get page ID and token
        with open(json_file_name, 'r') as f:
            data = json.load(f)

        page_token = data['page']['token']
        self.page_id = data['page']['id']

        self.graph = facebook.GraphAPI(access_token=page_token, version=version)

    def monthly_posts(self, year, month):
        last_day_in_month = calendar.monthrange(year, month)[1]
        return self.graph.get_all_connections(id=self.page_id,
                                              connection_name='posts',
                                              fields='type, name, created_time, object_id',
                                              since=datetime(year, month, 1, 0, 0, 0),
                                              until=datetime(year, month, last_day_in_month, 0, 0, 0))

    def post_life_time_insights(self, post_id, metric):
        return self.graph.get_connections(id=post_id,
                                          connection_name='insights',
                                          metric=metric,
                                          period='lifetime',
                                          show_description_from_api_doc=True)

    def write_posts_insights_into_csv(self, year, month):
        df_posts = pd.DataFrame(columns=pd.MultiIndex(levels=[[], []], labels=[[], []]))
        posts = self.monthly_posts(year, month)

        # -------------------------------------------------- POST INFO -------------------------------------------------
        post_id, created_time, post_type, post_name = list(), list(), list(), list()

        # -------------------------------------------------- ACTIVITY --------------------------------------------------
        activity_value, activity_unique_value = list(), list()
        share, like, comment = list(), list(), list()
        share_unique, like_unique, comment_unique = list(), list(), list()

        # --------------------------------------------------- CLICKS ---------------------------------------------------
        clicks_value, clicks_unique_value = list(), list()
        clicks_by_type_video_play, clicks_by_type_other, clicks_by_type_link = list(), list(), list()

        # ------------------------------------------------- IMPRESSIONS ------------------------------------------------
        impressions_value, impressions_unique_value = list(), list()
        impressions_fan_value, impressions_fan_unique_value = list(), list()

        # ------------------------------------------------- ENGAGEMENT -------------------------------------------------
        engaged_users_value, negative_feedback_value, negative_feedback_unique_value = list(), list(), list()

        # -------------------------------------------------- REACTIONS -------------------------------------------------
        reactions_like_total_value, reactions_love_total_value, reactions_wow_total_value = list(), list(), list()
        reactions_haha_total_value, reactions_sorry_total_value, reactions_anger_total_value = list(), list(), list()

        # ---------------------------------------------------- VIDEO ---------------------------------------------------
        video_avg_time_watched_value, video_complete_views_organic_value = list(), list()
        video_complete_views_organic_unique_value, video_views_organic_value = list(), list()
        video_views_organic_unique_value, video_views_value = list(), list()
        video_views_unique_value, video_view_time_value = list(), list()

        for ind, post in enumerate(posts):
            print(ind, post)

            post_id.append(post['id'])
            created_time.append(post['created_time'][:16])
            post_type.append(post['type'])
            try:
                post_name.append(post['name'])
            except KeyError:
                post_name.append('None')

            # ------------------------------------------------ ACTIVITY ------------------------------------------------
            # The number of stories generated about your Page post. (Total Count)
            activity = self.post_life_time_insights(post['id'], 'post_activity')
            try:
                activity_value.append(activity['data'][0]['values'][0]['value'])
            except KeyError:
                activity_value.append(0)

            # The number of unique people who created a story by interacting with your Page post. (Unique Users)
            activity_unique = self.post_life_time_insights(post['id'], 'post_activity_unique')
            try:
                activity_unique_value.append(activity_unique['data'][0]['values'][0]['value'])
            except KeyError:
                activity_unique_value.append(0)

            # The number of stories created about your Page post, by action type. (Total Count)
            activity_by_action_type = self.post_life_time_insights(post['id'], 'post_activity_by_action_type')
            try:
                share.append(activity_by_action_type['data'][0]['values'][0]['value']['share'])
            except KeyError:
                share.append(0)
            try:
                like.append(activity_by_action_type['data'][0]['values'][0]['value']['like'])
            except KeyError:
                like.append(0)
            try:
                comment.append(activity_by_action_type['data'][0]['values'][0]['value']['comment'])
            except KeyError:
                comment.append(0)

            # The number of unique people who created a story about your Page post by interacting with it. (Unique Users)
            activity_by_action_type_unique = self.post_life_time_insights(post['id'], 'post_activity_by_action_type_unique')
            try:
                share_unique.append(activity_by_action_type_unique['data'][0]['values'][0]['value']['share'])
            except KeyError:
                share_unique.append(0)
            try:
                like_unique.append(activity_by_action_type_unique['data'][0]['values'][0]['value']['like'])
            except KeyError:
                like_unique.append(0)
            try:
                comment_unique.append(activity_by_action_type_unique['data'][0]['values'][0]['value']['comment'])
            except KeyError:
                comment_unique.append(0)

            # ------------------------------------------------- CLICKS -------------------------------------------------
            # The number of clicks anywhere in your post on News Feed from the user that matched the audience targeting on it.
            # (Total Count)
            clicks = self.post_life_time_insights(post['id'], 'post_clicks')
            try:
                clicks_value.append(clicks['data'][0]['values'][0]['value'])
            except KeyError:
                clicks_value.append(0)

            # The number of clicks anywhere in your post on News Feed from the user that matched the audience targeting on it.
            # (Total Count)
            clicks_unique = self.post_life_time_insights(post['id'], 'post_clicks_unique')
            try:
                clicks_unique_value.append(clicks_unique['data'][0]['values'][0]['value'])
            except KeyError:
                clicks_unique_value.append(0)

            # The number of clicks anywhere in the post on News Feed from users that matched the audience targeting on the post,
            #  by type. (Total Count)
            clicks_by_type = self.post_life_time_insights(post['id'], 'post_clicks_by_type')
            try:
                clicks_by_type_video_play.append(clicks_by_type['data'][0]['values'][0]['value']['video play'])
            except KeyError:
                clicks_by_type_video_play.append(0)
            try:
                clicks_by_type_other.append(clicks_by_type['data'][0]['values'][0]['value']['other clicks'])
            except KeyError:
                clicks_by_type_other.append(0)
            try:
                clicks_by_type_link.append(clicks_by_type['data'][0]['values'][0]['value']['link clicks'])
            except KeyError:
                clicks_by_type_link.append(0)

            # ---------------------------------------------- IMPRESSIONS -----------------------------------------------
            # The number of times your Page's post entered a person's screen. Posts include statuses, photos, links, videos
            # and more. (Total Count)
            impressions = self.post_life_time_insights(post['id'], 'post_impressions')
            try:
                impressions_value.append(impressions['data'][0]['values'][0]['value'])
            except KeyError:
                impressions_value.append(0)

            # The number of people who had your Page's post enter their screen. Posts include statuses, photos, links, videos
            # and more. (Unique Users)
            impressions_unique = self.post_life_time_insights(post['id'], 'post_impressions_unique')
            try:
                impressions_unique_value.append(impressions_unique['data'][0]['values'][0]['value'])
            except KeyError:
                impressions_unique_value.append(0)

            # The number of impressions of your Page post to people who have liked your Page. (Total Count)
            impressions_fan = self.post_life_time_insights(post['id'], 'post_impressions_fan')
            try:
                impressions_fan_value.append(impressions_fan['data'][0]['values'][0]['value'])
            except KeyError:
                impressions_fan_value.append(0)

            # The number of people who saw your Page post because they've liked your Page (Unique Users)
            impressions_fan_unique = self.post_life_time_insights(post['id'], 'post_impressions_fan_unique')
            try:
                impressions_fan_unique_value.append(impressions_fan_unique['data'][0]['values'][0]['value'])
            except KeyError:
                impressions_fan_unique_value.append(0)

            # ----------------------------------------------- ENGAGEMENT -----------------------------------------------
            # The number of unique people who engaged in certain ways with your Page post, for example by commenting on, liking,
            # sharing, or clicking upon particular elements of the post. (Unique Users)
            engaged_users = self.post_life_time_insights(post['id'], 'post_engaged_users')
            try:
                engaged_users_value.append(engaged_users['data'][0]['values'][0]['value'])
            except KeyError:
                engaged_users_value.append(0)

            # The number of times people have given negative feedback to your post. (Total Count)
            negative_feedback = self.post_life_time_insights(post['id'], 'post_negative_feedback')
            try:
                negative_feedback_value.append(negative_feedback['data'][0]['values'][0]['value'])
            except KeyError:
                negative_feedback_value.append(0)

            # The number of people who have given negative feedback to your post. (Unique Users)
            negative_feedback_unique = self.post_life_time_insights(post['id'], 'post_negative_feedback_unique')
            try:
                negative_feedback_unique_value.append(negative_feedback_unique['data'][0]['values'][0]['value'])
            except KeyError:
                negative_feedback_unique_value.append(0)

            # ----------------------------------------------- REACTIONS ------------------------------------------------
            # Total like reactions of a post
            reactions_like_total = self.post_life_time_insights(post['id'], 'post_reactions_like_total')
            try:
                reactions_like_total_value.append(reactions_like_total['data'][0]['values'][0]['value'])
            except KeyError:
                reactions_like_total_value.append(0)

            # Total love reactions of a post
            reactions_love_total = self.post_life_time_insights(post['id'], 'post_reactions_love_total')
            try:
                reactions_love_total_value.append(reactions_love_total['data'][0]['values'][0]['value'])
            except KeyError:
                reactions_love_total_value.append(0)

            # Total wow reactions of a post
            reactions_wow_total = self.post_life_time_insights(post['id'], 'post_reactions_wow_total')
            try:
                reactions_wow_total_value.append(reactions_wow_total['data'][0]['values'][0]['value'])
            except KeyError:
                reactions_wow_total_value.append(0)

            # Total haha reactions of a post
            reactions_haha_total = self.post_life_time_insights(post['id'], 'post_reactions_haha_total')
            try:
                reactions_haha_total_value.append(reactions_haha_total['data'][0]['values'][0]['value'])
            except KeyError:
                reactions_haha_total_value.append(0)

            # Total sorry reactions of a post
            reactions_sorry_total = self.post_life_time_insights(post['id'], 'post_reactions_sorry_total')
            try:
                reactions_sorry_total_value.append(reactions_sorry_total['data'][0]['values'][0]['value'])
            except KeyError:
                reactions_sorry_total_value.append(0)

            # Total anger reactions of a post
            reactions_anger_total = self.post_life_time_insights(post['id'], 'post_reactions_anger_total')
            try:
                reactions_anger_total_value.append(reactions_anger_total['data'][0]['values'][0]['value'])
            except KeyError:
                reactions_anger_total_value.append(0)

            # -------------------------------------------------- VIDEO -------------------------------------------------
            if post['type'] == 'video':

                # Average time (in ms) video viewed (Total Count)
                video_avg_time_watched = self.post_life_time_insights(post['id'], 'post_video_avg_time_watched')
                try:
                    video_avg_time_watched_value.append(video_avg_time_watched['data'][0]['values'][0]['value'])
                except KeyError:
                    video_avg_time_watched_value.append(0)

                # Number of times your video was viewed to 95% of its length without any paid promotion. (Total Count)
                video_complete_views_organic = self.post_life_time_insights(post['id'], 'post_video_complete_views_organic')
                try:
                    video_complete_views_organic_value.append(video_complete_views_organic['data'][0]['values'][0]['value'])
                except KeyError:
                    video_complete_views_organic_value.append(0)

                # Number of times your video was viewed to 95% of its length without any paid promotion. (Unique Users)
                video_complete_views_organic_unique = self.post_life_time_insights(post['id'],
                                                                              'post_video_complete_views_organic_unique')
                try:
                    video_complete_views_organic_unique_value.append(video_complete_views_organic_unique['data'][0]['values'][0]['value'])
                except KeyError:
                    video_complete_views_organic_unique_value.append(0)

                # Number of times your video was viewed to 95% of its length without any paid promotion. (Unique Users)
                video_views_organic = self.post_life_time_insights(post['id'], 'post_video_views_organic')
                try:
                    video_views_organic_value.append(video_views_organic['data'][0]['values'][0]['value'])
                except KeyError:
                    video_views_organic_value.append(0)

                # Number of times your video was viewed for more than 3 seconds without any paid promotion. (Unique Users)
                video_views_organic_unique = self.post_life_time_insights(post['id'], 'post_video_views_organic_unique')
                try:
                    video_views_organic_unique_value.append(video_views_organic_unique['data'][0]['values'][0]['value'])
                except KeyError:
                    video_views_organic_unique_value.append(0)

                # Total number of times your video was viewed for more than 3 seconds. (Total Count)
                video_views = self.post_life_time_insights(post['id'], 'post_video_views')
                try:
                    video_views_value.append(video_views['data'][0]['values'][0]['value'])
                except KeyError:
                    video_views_value.append(0)

                # Number of unique people who viewed your video for more than 3 seconds. (Unique Users)
                video_views_unique = self.post_life_time_insights(post['id'], 'post_video_views_unique')
                try:
                    video_views_unique_value.append(video_views_unique['data'][0]['values'][0]['value'])
                except KeyError:
                    video_views_unique_value.append(0)

                # Total time (in ms) video has been viewed (Total Count)
                video_view_time = self.post_life_time_insights(post['id'], 'post_video_view_time')
                try:
                    video_view_time_value.append(video_view_time['data'][0]['values'][0]['value'])
                except KeyError:
                    video_view_time_value.append(0)

            else:
                video_avg_time_watched_value.append('na')
                video_complete_views_organic_value.append('na')
                video_complete_views_organic_unique_value.append('na')
                video_views_organic_value.append('na')
                video_views_organic_unique_value.append('na')
                video_views_value.append('na')
                video_views_unique_value.append('na')
                video_view_time_value.append('na')

        # ------------------------------------------------- POST INFO --------------------------------------------------
        df_posts['post', 'created_time'] = pd.Series(data=created_time, index=post_id, name='created_time')
        df_posts['post', 'type'] = pd.Series(data=post_type, index=post_id, name='type')
        df_posts['post', 'name'] = pd.Series(data=post_name, index=post_id, name='name')

        # -------------------------------------------------- ACTIVITY --------------------------------------------------
        df_posts['activity', 'value'] = pd.Series(data=activity_value, index=post_id, name='value')
        df_posts['activity_unique', 'value'] = pd.Series(data=activity_unique_value, index=post_id, name='value')

        df_posts['activity_by_action_type', 'share'] = pd.Series(data=share, index=post_id, name='share')
        df_posts['activity_by_action_type', 'like'] = pd.Series(data=like, index=post_id, name='like')
        df_posts['activity_by_action_type', 'comment'] = pd.Series(data=comment, index=post_id, name='comment')

        df_posts['activity_by_action_type_unique', 'share'] = pd.Series(data=share_unique, index=post_id, name='share')
        df_posts['activity_by_action_type_unique', 'like'] = pd.Series(data=like_unique, index=post_id, name='like')
        df_posts['activity_by_action_type_unique', 'comment'] = pd.Series(data=comment_unique, index=post_id, name='comment')

        # --------------------------------------------------- CLICKS ---------------------------------------------------
        df_posts['clicks', 'value'] = pd.Series(data=clicks_value, index=post_id, name='value')
        df_posts['clicks_unique', 'value'] = pd.Series(data=clicks_unique_value, index=post_id, name='value')

        df_posts['clicks_by_type', 'video_play'] = pd.Series(data=clicks_by_type_video_play, index=post_id, name='video_play')
        df_posts['clicks_by_type', 'other'] = pd.Series(data=clicks_by_type_other, index=post_id, name='other')
        df_posts['clicks_by_type', 'link'] = pd.Series(data=clicks_by_type_link, index=post_id, name='link')

        # ------------------------------------------------- IMPRESSIONS ------------------------------------------------
        df_posts['impressions', 'value'] = pd.Series(data=impressions_value, index=post_id, name='value')
        df_posts['impressions_unique', 'value'] = pd.Series(data=impressions_unique_value, index=post_id, name='value')

        df_posts['impressions_fan', 'value'] = pd.Series(data=impressions_fan_value, index=post_id, name='value')
        df_posts['impressions_fan_unique', 'value'] = pd.Series(data=impressions_fan_unique_value, index=post_id, name='value')

        # ------------------------------------------------- ENGAGEMENT -------------------------------------------------
        df_posts['engaged_users', 'value'] = pd.Series(data=engaged_users_value, index=post_id, name='value')
        df_posts['negative_feedback', 'value'] = pd.Series(data=negative_feedback_value, index=post_id, name='value')
        df_posts['negative_feedback_unique', 'value'] = pd.Series(data=negative_feedback_unique_value, index=post_id, name='value')

        # -------------------------------------------------- REACTIONS -------------------------------------------------
        df_posts['reactions_like', 'value'] = pd.Series(data=reactions_like_total_value, index=post_id, name='value')
        df_posts['reactions_love', 'value'] = pd.Series(data=reactions_love_total_value, index=post_id, name='value')
        df_posts['reactions_wow', 'value'] = pd.Series(data=reactions_wow_total_value, index=post_id, name='value')
        df_posts['reactions_haha', 'value'] = pd.Series(data=reactions_haha_total_value, index=post_id, name='value')
        df_posts['reactions_sorry', 'value'] = pd.Series(data=reactions_sorry_total_value, index=post_id, name='value')
        df_posts['reactions_anger', 'value'] = pd.Series(data=reactions_anger_total_value, index=post_id, name='value')

        # ---------------------------------------------------- VIDEO ---------------------------------------------------
        df_posts['video', 'avg_time_watched'] = pd.Series(data=video_avg_time_watched_value, index=post_id, name='avg_time_watched')
        df_posts['video', 'complete_views_organic'] = pd.Series(data=video_complete_views_organic_value, index=post_id, name='complete_views_organic')
        df_posts['video', 'complete_views_organic_unique'] = pd.Series(data=video_complete_views_organic_unique_value, index=post_id, name='complete_views_organic_unique')
        df_posts['video', 'views_organic'] = pd.Series(data=video_views_organic_value, index=post_id, name='views_organic')
        df_posts['video', 'organic_unique'] = pd.Series(data=video_views_organic_unique_value, index=post_id, name='organic_unique')
        df_posts['video', 'views'] = pd.Series(data=video_views_value, index=post_id, name='views')
        df_posts['video', 'views_unique'] = pd.Series(data=video_views_unique_value, index=post_id, name='views_unique')
        df_posts['video', 'view_time'] = pd.Series(data=video_view_time_value, index=post_id, name='view_time')

        df_posts.to_csv(f'Posts_insights_{year}_{month}.csv')


def main():
    # TODO: use the latest version available
    app = PageApp('facebook.json', version="3.1")

    # TODO: change the year and month to get insights for a specific month in a pacific year
    app.write_posts_insights_into_csv(2019, 1)


if __name__ == '__main__':
    main()