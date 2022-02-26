import pygame


def dijkstra(queue, path, start_box, target_box):
    if len(queue) > 0:
        current_box = queue.pop(0)
        current_box.visited = True
        if current_box == target_box:
            print("A solution was found.")
            while current_box.prior != start_box:
                path.append(current_box.prior)
                current_box = current_box.prior
            return
        else:
            for neighbour in current_box.neighbours:
                if not neighbour.queued and not neighbour.wall:
                    neighbour.prior = current_box
                    neighbour.queued = True
                    queue.append(neighbour)