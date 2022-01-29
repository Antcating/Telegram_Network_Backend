import asyncio
import os

import pickle
import networkx as nx
import telethon
import questionary
from total_database import total_database_operation
from message_parser import parse_messages
from graph_processing import networkx_nodes, graph_export


async def main(client):
    """
    Main function of the graph processing. \n
    - Gets client and tries to connect \n
    - Manage last channel database and saves the last after each iteration to `db.pkl` \n
    - Manage total graph and saves the composed graph after each iteration to `graph.p` \n
    - Manage last link and saves the last link after each iteration to `last` \n
    :param client: TelegramClient
    :return:
    """
    await client.connect()
    try:
        while True:
            now_loop_link = await total_database_operation(client)
            df_forward_channels = await parse_messages(client, now_loop_link)
            if df_forward_channels is None:
                with open('last', 'w') as last_loop:
                    last_loop.write(now_loop_link)
                continue
            df_forward_channels.to_pickle('db.pkl')
            # df_forward_channels = pd.read_pickle('dummy_db.pkl')
            graph = await networkx_nodes(df_forward_channels)
            try:
                graph_main = pickle.load(open("graph.p", "rb"))
                graph_main = nx.compose(graph_main, graph)
                pickle.dump(graph_main, open("graph.p", "wb"))
            except FileNotFoundError:
                pickle.dump(graph, open("graph.p", "wb"))

            with open('last', 'w') as last_loop:
                last_loop.write(now_loop_link)
    except asyncio.CancelledError:

        await client.disconnect()
    except KeyboardInterrupt:
        return now_loop_link


if __name__ == '__main__':
    try:
        main_mode = questionary.select(
            "What do you want to do?",
            choices=[
                'Graph processing',
                'Map HTML export',
            ]).ask()
        if main_mode == 'Graph processing':
            api_id = int(questionary.password('Api ID:').ask())
            api_hash = questionary.password('Api hash:').ask()
            client = telethon.TelegramClient('upd_tel_net', api_id, api_hash)

            asyncio.run(main(client))
        elif main_mode == 'Map HTML export':
            graph_main = pickle.load(open("graph.p", "rb"))
            graph_export(graph_main)
    except KeyboardInterrupt:
        try:
            sv = questionary.confirm("\nSave result to the next session?").ask()
            if sv:
                print('Saved!')
            else:
                try:
                    os.remove('graph.p')
                except FileNotFoundError:
                    pass
        except FileNotFoundError:
            pass
