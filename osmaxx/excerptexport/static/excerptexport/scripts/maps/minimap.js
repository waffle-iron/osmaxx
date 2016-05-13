'use strict';

(function(){
    jQuery("div[id^='minimap']").each(function(discarded, elem){
        var id = elem.id.replace('minimap-', '');
        var excerpt = new ExcerptViewer(
            elem.id,
            "/api/bounding_geometry_from_excerpt/{ID}/"
        );
        excerpt.showExcerptOrCountryOnMap(id);
    });
})();

