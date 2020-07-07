#ifndef PRIORITIZEDPLANNING_H
#define PRIORITIZEDPLANNING_H

#include "config.h"
#include "agent_set.h"
#include "map.h"
#include "isearch.h"
#include "astar.h"
#include "multiagent_search_result.h"
#include "multiagent_search_inteface.h"
#include <vector>

class PrioritizedPlanning : public MultiagentSearchInterface
{
public:
    PrioritizedPlanning();
    PrioritizedPlanning(ISearch<>* Search);
    ~PrioritizedPlanning(void);
    MultiagentSearchResult startSearch(const Map &map, const Config &config, AgentSet &AgentSet) override;

private:
    ISearch<>*                      search;
};

#endif // PRIORITIZEDPLANNING_H
