try:
  client = carla.Client("localhost", 2000)
  world = client.get_world()

  walker_bp = world.get_blueprint_library().filter("walker.pedestrian.*")
  controller_bp = world.get_blueprint_library().find('controller.ai.walker')
  
  actors = []
  for i in range(200):
    # location
    trans = carla.Transform()
    trans.location = world.get_random_location_from_navigation()
    trans.location.z += 1

    # walker actor
    walker = random.choice(walker_bp)
    actor = world.spawn_actor(walker, trans)
    world.wait_for_tick()

    # walker AI controller
    controller = world.spawn_actor(controller_bp, carla.Transform(), actor)
    world.wait_for_tick()
    
    # managing pedestrian through controller
    controller.start()
    controller.go_to_location(world.get_random_location_from_navigation())

    actors.append(actor)
    actors.append(controller)

  while (1):
    time.sleep(0.1)
    
finally:
  client.apply_batch([carla.command.DestroyActor(x) for x in actors])
