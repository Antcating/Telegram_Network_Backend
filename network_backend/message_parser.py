import pandas as pd
import telethon, scipy
import asyncio, sys
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors.rpcerrorlist import RpcCallFailError


async def parse_messages(client,
                         now_loop_link):
    """
    Parses channel messages. Looks for message.forward.from_id.
    - Manage df_forward_channels - dataframe with connections between channel and forward channels
    - Manage total list of channels (for subsequent iterations) ant saves it to `total_list.csv`
    :return: Dataframe
    """
    df_forward_channels = pd.DataFrame(columns=[
        # 'channel_origin_title',
        # 'channel_origin_link',
        # 'channel_origin_members',
        # 'channel_origin_count',

        'channel_forward_id',
        'channel_forward_title',
        'channel_forward_link',
        'channel_forward_members',
        'channel_forward_count',

        'channel_origin'])
    df_total_channels = pd.read_csv('total_list.csv')
    channel = await client.get_entity(now_loop_link)
    origin_channel_internal = await client(GetFullChannelRequest(channel.id))
    if not origin_channel_internal.chats[0].broadcast:  # If it is a group connected to the channel - skip it
        return None
    origin_channel_id = origin_channel_internal.chats[0].id
    origin_channel_title = origin_channel_internal.chats[0].title
    origin_channel_link = origin_channel_internal.chats[0].username
    origin_channel_members = origin_channel_internal.full_chat.participants_count

    origin_channel_count = 0

    df_forward_channels.loc[0] = [
        origin_channel_id,
        origin_channel_title,
        origin_channel_link,
        origin_channel_members,
        origin_channel_count,

        1
    ]
    bar = [
        " ...",
        " ",
    ]
    n_message = 0
    async for message in client.iter_messages(channel):
        if n_message == 0:
            total_messages = message.id
        n_message += 1
        sys.stdout.write(
            '\r' + 'Now: ' + now_loop_link + ': ' + str(1 + total_messages - message.id) + '/' + str(total_messages) + \
            '; Found: ' + str(origin_channel_count) + \
            ' Est. time: ' + str(round(message.id / 285, 2)) + ' min')
        sys.stdout.flush()
        if message.forward is not None and isinstance(message.forward.from_id, telethon.tl.types.PeerChannel):
            try:
                fwd_channel_internal = await client(GetFullChannelRequest(message.forward.from_id))
                if fwd_channel_internal.chats[0].broadcast:
                    fwd_channel_id = fwd_channel_internal.chats[0].id
                    fwd_channel_title = fwd_channel_internal.chats[0].title
                    fwd_channel_link = fwd_channel_internal.chats[0].username
                    fwd_channel_members = fwd_channel_internal.full_chat.participants_count

                    if fwd_channel_link is None:  # channel internal errors
                        continue
                    if fwd_channel_link not in df_forward_channels[
                        'channel_forward_id'].to_list():  # connections count
                        df_forward_channels.loc[len(df_forward_channels)] = [
                            fwd_channel_id,
                            fwd_channel_title,
                            fwd_channel_link,
                            fwd_channel_members,
                            1,

                            0
                        ]
                    else:
                        df_forward_channels.loc[
                            df_forward_channels['channel_forward_id'] == fwd_channel_id, 'channel_forward_count'] = \
                            df_forward_channels.loc[df_forward_channels[
                                                        'channel_forward_id'] == fwd_channel_id, 'channel_forward_count'] + 1

                    if fwd_channel_id not in df_total_channels['id'].to_list():  # total list processing
                        df_total_channels.loc[len(df_total_channels)] = [
                            fwd_channel_id,
                            fwd_channel_title,
                            fwd_channel_link,
                            fwd_channel_members,
                        ]
                    origin_channel_count += 1
            except RpcCallFailError:  # Internal Telegram issues
                await asyncio.sleep(2)
            except telethon.errors.ChannelPrivateError:
                pass
            except telethon.errors.ChannelBannedError:
                pass
            except KeyboardInterrupt:
                return KeyboardInterrupt
        n_message += 1
        await asyncio.sleep(0.2001)     # Telegram limitations
    df_total_channels.to_csv('total_list.csv', index=False)
    return df_forward_channels
