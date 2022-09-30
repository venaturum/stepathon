from folium.plugins.timestamped_geo_json import Map, TimestampedGeoJson

from stepathon.api import maps_from_coords_and_steps


def _patch_TimestampedGeoJson():

    from folium.plugins.timestamped_geo_json import Template

    TimestampedGeoJson._template = Template(
        """
        {% macro script(this, kwargs) %}
            L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
                _getDisplayDateFormat: function(date){
                    var newdate = new moment(date);
                    console.log(newdate)
                    return newdate.format("{{this.date_options}}");
                }
            });
            {{this._parent.get_name()}}.timeDimension = L.timeDimension(
                {
                    period: {{ this.period|tojson }},
                }
            );
            var timeDimensionControl = new L.Control.TimeDimensionCustom(
                {{ this.options|tojson }}
            );
            {{this._parent.get_name()}}.addControl(this.timeDimensionControl);

            var geoJsonLayer = L.geoJson({{this.data}}, {
                    pointToLayer: function (feature, latLng) {
                        if (feature.properties.icon == 'marker') {
                            if(feature.properties.iconstyle){
                                return new L.Marker(latLng, {
                                    icon: L.icon(feature.properties.iconstyle)});
                            }
                            //else
                            return new L.Marker(latLng);
                        }
                        if (feature.properties.icon == 'circle') {
                            if (feature.properties.iconstyle) {
                                return new L.circleMarker(latLng, feature.properties.iconstyle)
                                };
                            //else
                            return new L.circleMarker(latLng);
                        }
                        //else

                        return new L.Marker(latLng);
                    },
                    style: function (feature) {
                        return feature.properties.style;
                    },
                    onEachFeature: function(feature, layer) {
                        if (feature.properties.popup) {
                        layer.bindPopup(feature.properties.popup);
                        }
                        if (feature.properties.tooltip) {
                        layer.bindTooltip(feature.properties.tooltip);
                        }
                    }
                })

            var {{this.get_name()}} = L.timeDimension.layer.geoJson(
                geoJsonLayer,
                {
                    updateTimeDimension: true,
                    addlastPoint: {{ this.add_last_point|tojson }},
                    duration: {{ this.duration }},
                }
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """
    )  # noqa


_patch_TimestampedGeoJson()
