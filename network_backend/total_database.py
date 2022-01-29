import pandas as pd
from telethon.tl.functions.channels import GetFullChannelRequest


async def total_database_operation(client):
    try:
        df_total_links = pd.read_csv('total_list.csv')
        try:
            with open("last", "r") as last_channel_checked:
                indexed_last_list = df_total_links[df_total_links['link'] == last_channel_checked.read().strip()]
                now_index = indexed_last_list.index.astype(int) + 1
                now_loop_link = df_total_links.loc[now_index]['link'].to_string(index=False)
                if 'Series([]' in now_loop_link:
                    raise FileNotFoundError
                print('\nThe link -> %s <- was taken' % now_loop_link)
                return now_loop_link
        except KeyError:
            print('\nLast checked link was the last in the total link list')
            return KeyError
        except FileNotFoundError:
            now_loop_link = df_total_links['link'][0]
            print('\nThe link -> %s <- was taken' % now_loop_link)
            return now_loop_link
    except FileNotFoundError:
        now_loop_link = input('Enter first link (format: ONLY USERNAME): ')

        channel = await client.get_entity(now_loop_link)
        origin_channel_internal = await client(GetFullChannelRequest(channel.id))

        origin_channel_id = origin_channel_internal.chats[0].id
        origin_channel_title = origin_channel_internal.chats[0].title
        origin_channel_link = origin_channel_internal.chats[0].username
        origin_channel_members = origin_channel_internal.full_chat.participants_count

        df_total_links = pd.DataFrame(columns=['id','title', 'link', 'members'])
        df_total_links.loc[0] = [
            origin_channel_id,
            origin_channel_title,
            origin_channel_link,
            origin_channel_members,
        ]
        df_total_links.to_csv('total_list.csv', index=False)
        return now_loop_link
