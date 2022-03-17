# vkapi

<details>
  <summary>Example</summary>
  
  ```python
    from vkapi import Vk, Longpoll

    vk = Vk('<your access_token>').get_api()


    for event in Longpoll.listen(vk):
      if event[0] == 4 and event[3] - 2_000_000_000 > 0 and event[5] == 'мяу':
        vk.messages.send(
          message='мур',
          peer_id=event[3],
          random_id=random.randint(0, 2_147_483_647 )
        )
  ```
</details>
