#ifndef SIPP_H
#define SIPP_H

#include "astar.h"

class SIPP : private Astar
{
public:
    SIPP();

    std::list<Node> findSuccessors(const Node &curNode, const Map &map, int goal_i = 0, int goal_j = 0, int agentId = -1,
                                                   const std::unordered_set<Node> &occupiedNodes = std::unordered_set<Node>(),
                                                   const ConstraintsSet &constraints = ConstraintsSet(),
                                                   const ConflictAvoidanceTable &CAT = ConflictAvoidanceTable()) override;
};

#endif // SIPP_H