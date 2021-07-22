import math


def reward_function(params):
    # Read input parameters
    steering = abs(params['steering_angle'])  # Only need the absolute steering angle
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    all_wheels_on_track = params['all_wheels_on_track']

    # Initialize reward
    reward = 1

    # Steering penalty threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15

    if not all_wheels_on_track:
        reward = 1e-3  # Penalize if the car goes off track
    else:
        reward *=2
        
        # Penalize reward if the agent is steering too much
        if steering > ABS_STEERING_THRESHOLD:
            reward *= 0.8
        else:
            reward *= 1.2
            
        # Calculate the direction of the center line based on the closest waypoints
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]
    
        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] -
        prev_point[0])
    
        # Convert to degree
        track_direction = math.degrees(track_direction)
    
        # Calculate the difference between the track direction and the heading direction of the car
        direction_diff = abs(track_direction - heading)
        if direction_diff > 180:
            direction_diff = 360 - direction_diff
        
        # Penalize the reward if the difference is too large
        DIRECTION_THRESHOLD = 10.0
        if direction_diff > DIRECTION_THRESHOLD:
            reward *= 0.5
        elif direction_diff <= DIRECTION_THRESHOLD:
            reward *= 2
            if params['speed'] < 2:
                reward *= 0.9  # Penalize if the car goes too slow
            elif params['speed'] >= 3:
                reward *= 1.5  # Higher reward if the car stays on track and goes fast


    # Reward track completion
    if params['progress'] >= 100:
        reward += 10000

    return float(reward)
