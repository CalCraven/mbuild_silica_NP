"""
Primary function of recipe here
"""

import mbuild as mb
import numpy as np
from numpy import sqrt, pi, arctan2, arcsin

class build_silica_NP(mb.Compound):
    """
    Build a tethered_NP compound. 
    Example would be a silica nanoparticle covered in alkane chains

    Parameters
    ----------
    Args:
    n_core_particles (int): Number of particles that makes up the central NP
    ball_radius (float): Radius of the nanoparticle.
    n_chains (int): Number of chains to attach to the nanoparticle.
    chain_length (int): Length of the chains being attached.
    monomer (Compound, optional): Type of chain being attached

    """
    def __init__(self, n_core_particles=129,  ball_radius=10, n_chains=4,
            chain_length=10, monomer=None):
        #n_core_particles can be related to the radius by a percent area
        super(build_silica_NP, self).__init__()
        
        class Bead(mb.Compound):
            """A point particle with two ports pointing in opposite directions"""
            def __init__(self,particle_kind):
                super(Bead,self).__init__()
                self.add(mb.Particle(name=particle_kind), particle_kind)

                self.add(mb.Port(anchor=self.labels[particle_kind]),'up')
                self['up'].translate(np.array([0, 0.7, 0]))

                self.add(mb.Port(anchor=self.labels[particle_kind]), 'down')
                self['down'].translate(np.array([0, -0.7, 0]))


        """Create a cg bead to use as the NP chains"""
        if not monomer:
            monomer = Bead(particle_kind='chain_monomer')

        """Create the particles that make up the core sphere"""
        class Sphere(mb.Compound):
            def __init__(self, n=65, radius=1, port_distance_from_surface=0.07):
                """Initialize a sphere object
                Args:
                n (int): Number of points used to construct the Sphere
                radius (float, nm): Radius of the sphere from np center to center of CG particles
                port_distance_from_surface (float, nm): Distance of Sphere Ports
                """
                super(Sphere,self).__init__()
                particle = mb.Particle(name='np')
                particle.add(mb.Port(anchor=particle), label='out')

                #Generate points on sphere surface
                pattern=mb.SpherePattern(n)
                pattern.scale(radius)

                particles=pattern.apply(particle, orientation='normal', compound_port='out')
                self.add(particles, label='np_[$]')

                #Create particles and Ports at pattern positions
                for i, pos in enumerate(pattern.points):
                    particle = mb.Particle(name="np",pos=pos)
                    self.add(particle, "np_{}".format(i))
                    port=mb.Port(anchor=particle)
                    self.add(port, "port_{}".format(i))

                    #Make the top of the port point towards the positive x axis
                    port.spin(-pi/2, [0,0,1])
                    #Raise up or down the top of the port in the z direction
                    port.spin(-arcsin(pos[2]/radius), [0, 1, 0])
                    #rotate the port along the z axis
                    port.spin(arctan2(pos[1], pos[0]), [0, 0, 1])
                    #Move the Port a bit away from the surface of the Sphere
                    port.translate(pos/radius * port_distance_from_surface)

        #Add in the correct number of particles around a sphere
        self.add(Sphere(n=n_core_particles, radius=ball_radius,
                port_distance_from_surface=0.7), label="np")

        # Generate points on the surface of a unit sphere to attach chains.
        pattern = mb.SpherePattern(n_chains)
    
        # Magnify it a bit.
        pattern.scale(ball_radius)

        chain_proto = mb.recipes.Polymer(monomer, n=chain_length)
    
        # Apply chains to pattern.
        chain_protos, empty_backfill = pattern.apply_to_compound(chain_proto,
            guest_port_name="down", host=self['np'])
    
        self.add(chain_protos)

        self.generate_bonds('np', 'np', sqrt(4 * ball_radius ** 2 * pi / n_core_particles) - 0.5,
            sqrt(4 * ball_radius**2 * pi / n_core_particles) + 0.5)
    
        self.generate_bonds('np', 'chain_monomer', 0.1, 0.3)
        self.generate_bonds('chain_monomer', 'np', 0.1, 0.3)
