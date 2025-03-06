#version 330 core

uniform sampler2D tex;
uniform float transposition_shader_multiplayer;
// uniform float time;

const vec2 u_resolution = vec2(640.,360.);

in vec2 uvs;
out vec4 f_color;

void main() {
    float adjusted_multiplayer = abs(transposition_shader_multiplayer)/2;
    float aspect = u_resolution.x / u_resolution.y;

    const float RADIUS = 2.;

    vec2 circle_centre = vec2(0.5145833333333333, 0.5296296296296296);
    vec2 ellipse_radii = vec2(RADIUS, RADIUS*aspect);  // Control the radii for X and Y directions

    float red = texture(tex, uvs).r;
    float green = texture(tex, uvs).g;
    float blue = texture(tex, uvs).b;

    // Compute distance in normalized coordinates for the ellipse
    vec2 normalized_coords = (uvs - circle_centre) / ellipse_radii;
    float disc = length(normalized_coords);

    disc = 4.0 * disc;

    if (disc > 1.0) {
        disc = 1.0;
    }

    float time = 1.;

    //debug
    // float old_disc = abs(disc - 1.0);

    disc = abs(disc - 1.0) * adjusted_multiplayer;

    float calibrated_time = abs(mod(time*10.,20.)-10.)+10.;

    float disc_yellow = max(0.04,(pow(disc, 3)+0.025)*(1*(calibrated_time/14)+1.45));
    
    float disc_blue = max(0.04,pow(disc/1.5, 3)+0.025);
    disc_yellow += 0.015;
    disc_blue += 0.005;



    //debug
    // if (old_disc > 0.95){
    //     disc_yellow = 1.;
    //     disc_blue = 1.;
    // }




    f_color = vec4(red * disc_yellow, green * disc_yellow, blue * disc_blue, 1.0);
}