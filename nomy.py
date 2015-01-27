import math

class Planet(object):

    def __init__(self, name, a,  e,  i,  l,  lp,  ln,
                             ac, ec, ic, lc, lpc, lnc):
        self.name = name
        self.a = a
        self.ac = ac
        self.e = e
        self.ec = ec
        self.i = i
        self.ic = ic
        self.l = l
        self.lc = lc
        self.lp = lp
        self.lpc = lpc
        self.ln = ln
        self.lnc = lnc

    def semi_major_axis(self, julian_date):
        return current_param(julian_date, self.a, self.ac)

    def eccentricity(self, julian_date):
        return current_param(julian_date, self.e, self.ec)

    def inclination(self, julian_date):
        return math.radians(current_param(julian_date, self.i, self.ic))

    def mean_longitude(self, julian_date):
        return math.radians(current_param(julian_date, self.l, self.lc))

    def longitude_perhelion(self, julian_date):
        return math.radians(current_param(julian_date, self.lp, self.lpc))

    def longitude_ascending(self, julian_date):
        return math.radians(current_param(julian_date, self.ln, self.lnc))

# Source: http://ssd.jpl.nasa.gov/?planet_pos
#                          a              e               I                L            long.peri.      long.node.
#                      AU, AU/Cy     rad, rad/Cy     deg, deg/Cy      deg, deg/Cy      deg, deg/Cy     deg, deg/Cy
#           -----------------------------------------------------------------------------------------------------------
planets = [
    Planet("Mercury",  0.38709927,     0.20563593,     7.00497902,     252.25032350,    77.45779628,    48.33076593,
                       0.00000037,     0.00001906,    -0.00594749,  149472.67411175,     0.16047689,    -0.12534081),
    Planet("Venus",    0.72333566,     0.00677672,     3.39467605,     181.97909950,   131.60246718,    76.67984255,
                       0.00000390,    -0.00004107,    -0.00078890,   58517.81538729,     0.00268329,    -0.27769418),
    Planet("Earth",    1.00000261,     0.01671123,    -0.00001531,     100.46457166,   102.93768193,     0.0,
                       0.00000562,    -0.00004392,    -0.01294668,   35999.37244981,     0.32327364,     0.0),
    Planet("Mars",     1.52371034,     0.09339410,     1.84969142,      -4.55343205,   -23.94362959,    49.55953891,
                       0.00001847,     0.00007882,    -0.00813131,   19140.30268499,     0.44441088,    -0.29257343),
    Planet("Jupiter",  5.20288700,     0.04838624,     1.30439695,      34.39644051,    14.72847983,   100.47390909,
                      -0.00011607,    -0.00013253,    -0.00183714,    3034.74612775,     0.21252668,     0.20469106),
    Planet("Saturn",   9.53667594,     0.05386179,     2.48599187,      49.95424423,    92.59887831,   113.66242448,
                      -0.00125060,    -0.00050991,     0.00193609,    1222.49362201,    -0.41897216,    -0.28867794),
    Planet("Uranus",  19.18916464,     0.04725744,     0.77263783,     313.23810451,   170.95427630,    74.01692503,
                      -0.00196176,    -0.00004397,    -0.00242939,     428.48202785,     0.40805281,     0.04240589),
    Planet("Neptune", 30.06992276,     0.00859048,     1.77004347,     -55.12002969,    44.96476227,   131.78422574,
                       0.00026291,     0.00005105,     0.00035372,     218.45945325,    -0.32241464,    -0.00508664),
    Planet("Pluto",   39.48211675,     0.24882730,    17.14001206,     238.92903833,   224.06891629,   110.30393684,
                      -0.00031596,     0.00005170,     0.00004818,     145.20780515,    -0.04062942,    -0.01183482),
]

# a semi major axis
# e eccentricity
# I inclination
# L mean longitude
# w longitude perihelion
# omega longitude ascending node
#
# w perihelion
# M mean anomaly
# E eccentric anomaly


def current_param(date, base, per_century):
    # centuries past J2000.0
    centuries = (date - 2451545.0) / 36525.
    return base + (per_century * centuries)

def solve_kepler(eccentricity, mean_anomaly):
    # for the approximate formulae in the present context, tol = 10e-6 degrees is sufficient
    tolerance = 10e-6
    # E0 = M + e sin M
    eccentric_anomaly = mean_anomaly + (eccentricity * math.sin(mean_anomaly))
    # and itterate the following equations with n = 0,1,2,... unitl |delta E| <= tol
    while True:
        # delta M = M - (En - e sin En)
        delta_mean_anomaly = mean_anomaly - (eccentric_anomaly - (eccentricity * math.sin(eccentric_anomaly)))
        # delta E = delta M / (1 - e cos En)
        delta_eccentric_anomaly = delta_mean_anomaly / (1 - (eccentricity * math.cos(eccentric_anomaly)))
        # En+1 = En + delta E
        eccentric_anomaly += delta_eccentric_anomaly

        if abs(delta_eccentric_anomaly) <= tolerance:
            return eccentric_anomaly

def orbital_coordinates(semi_major_axis, eccentricity, eccentric_anomaly):
    x = semi_major_axis * (math.cos(eccentric_anomaly) - eccentricity)
    y = semi_major_axis * math.sqrt(1 - (eccentricity ** 2)) * math.sin(eccentric_anomaly)
    return x, y

def ecliptic_coordinates(orbit_x, orbit_y, perihelion, longitude_ascending, inclination):
    term1 = math.cos(perihelion) * math.cos(longitude_ascending)
    term2 = math.sin(perihelion) * math.sin(longitude_ascending) * math.cos(inclination)
    term3 = math.sin(perihelion) * math.cos(longitude_ascending)
    term4 = math.cos(perihelion) * math.sin(longitude_ascending) * math.cos(inclination)
    x = (term1 - term2) * orbit_x + (-term3 - term4) * orbit_y

    term1 = math.cos(perihelion) * math.sin(longitude_ascending)
    term2 = math.sin(perihelion) * math.cos(longitude_ascending) * math.cos(inclination)
    term3 = math.sin(perihelion) * math.sin(longitude_ascending)
    term4 = math.cos(perihelion) * math.cos(longitude_ascending) * math.cos(inclination)
    y = (term1 + term2) * orbit_x + (-term3 + term4) * orbit_y

    term1 = math.sin(perihelion) * math.sin(inclination)
    term2 = math.cos(perihelion) * math.sin(inclination)
    z = term1 * orbit_x + term2 * orbit_y

    return x, y, z

def equatorial_coordinates(ecl_x, ecl_y, ecl_z, inclination):
    y = (math.cos(inclination) * ecl_y) - (math.sin(inclination) * ecl_z)
    z = (math.sin(inclination) * ecl_y) + (math.cos(inclination) * ecl_z)
    return ecl_x, y, z

def planet_position(planet, jd):
    perihelion = planet.longitude_perhelion(jd) - planet.longitude_ascending(jd)
    mean_anomaly = planet.mean_longitude(jd) - planet.longitude_perhelion(jd)
    eccentric_anomaly = solve_kepler(planet.eccentricity(jd), mean_anomaly)

    ox, oy = orbital_coordinates(planet.semi_major_axis(jd), planet.eccentricity(jd), eccentric_anomaly)
    return ox, oy, 0
    ecx, ecy, ecz = ecliptic_coordinates(ox, oy, perihelion, planet.longitude_ascending(jd), planet.inclination(jd))
    return ecx, ecy, ecz
    return equatorial_coordinates(ecx, ecy, ecz, planet.inclination(jd))
