from channels.testing import WebsocketCommunicator
from direct_messages.consumers import NotificationConsumer
from channels.layers import get_channel_layer
import json
import asyncio

class TestNotificationConsumer:
    async def test_notification_consumer(self):
        communicator = WebsocketCommunicator(NotificationConsumer, "/ws/notify/")
        print('connected')
        connected, _ = await communicator.connect()
        
        assert connected

        response = await communicator.receive_json_from()

        # Проверяем, что соединение установлено с ожидаемым ответом
        assert response == {'type': 'websocket.accept'}
        print(response, 'response')

        # Отправляем сообщение для обработки
        await communicator.send_json_to(
            {"type": "send_notification", "value": json.dumps({"count": 5})}
        )
        print('send')

        response = await communicator.receive_json_from()

        # Проверяем ответ на отправленное сообщение
        assert response == {'count': 5}

        await communicator.disconnect()

        disconnected, _ = await communicator.receive_output()
        
        # Проверяем, что отключения прошло успешно
        assert disconnected["type"] == "websocket.close"

        assert not communicator.connected
