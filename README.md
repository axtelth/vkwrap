# vkwrap

<details>
  <summary>Group bot example</summary>

  ```python
    from vkwrap import Vk, Longpoll
    from random import randint

    vk_session = Vk('<your group access_token>')
    vk = vk_session.get_api()
    longpoll = Longpoll(vk_session, '<your group id>')


    for event in longpoll.listen():
        if event['type'] == 'message_new' and event['object']['message']['text'] == 'мяу':
            vk.messages.send(
                message='мур',
                peer_id=event['object']['message']['peer_id'],
                random_id=randint(0, 2_147_483_647)
            )
  ```
</details>

<details>
  <summary>User bot example</summary>

  ```python
    from vkwrap import Vk, Longpoll
    from random import randint

    vk_session = Vk('<your access_token')
    vk = vk_session.get_api()
    longpoll = Longpoll(vk_session)

    for event in longpoll.listen():
        if event[0] == 4 and event[3] - 2_000_000_000 > 0 and event[6] == 'мяу':
            vk.messages.send(
                message='мур',
                peer_id=event[3],
                random_id=randint(0, 2_147_483_647)
            )
  ```
</details>
