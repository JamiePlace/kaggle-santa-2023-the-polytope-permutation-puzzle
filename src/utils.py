from pathlib import Path
from typing import List
from collections import deque


def get_project_root() -> Path:
    return Path(__file__).parent.parent

def cancel_pairs(moves:List[str]) -> str:
    pair = deque()
    group = deque()
    result = deque() 
    for move in moves:
        if len(pair)<1:
            pair.append(move)
            continue

        # grab and remove the previous move
        head = pair.pop()
        # check if the previous move is the inverse of the current move
        if head[1:] == move or move[1:]==head:
            continue
        # current move
        pair.append(move)

        if len(group)<1:
            group.append(head)
            continue

        # check if previous move is different to the last move of the group
        if head.replace('-','')[0] != group[-1].replace('-','')[0]:
            # store the group and start a new one at the previous move
            result.extend(group)
            group=deque([head])
            continue

        inverse_head = '-'+head if len(head)==2 else head[1:]
        # if we can find an inverse move in the group then remove it
        if inverse_head in group:
            group.remove(inverse_head)
        else:
            group.append(head)
     
    # Collect whatever is left over from the pairs and groups list
    if len(pair)>0:
        head = pair.pop()
        # check if previous move is different to the last move of the group
        if head.replace('-','') != group[-1].replace('-',''):
            result.extend(group)
            group=deque([head])
        else:
            positive_head = False if len(head.split("-")) == 2 else True
            inverse_head = '-'+head if positive_head else head
            if inverse_head in group:
                group.remove(inverse_head)
            else:
                group.append(head)
                
    if len(group)>0:
        result.extend(group)
        
    return '.'.join(result)
