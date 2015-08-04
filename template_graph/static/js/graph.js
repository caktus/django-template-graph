var create_graph = function(data, $graph_div) {
    graph = Viz(data, "svg");
    $graph_div.html(graph);
};
