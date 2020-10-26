###########################################################################################################################
###                                           Bates Model B, three boxes                                                ###
###########################################################################################################################
# Execute: $ python Bates_ModelB_3boxes.py -forcing custom --deltaQ_custom 1 1 1
#
# Conceptual model generalising Model B of Bates (2012) to three boxes:
# a northern polar box, a southern polar box and a tropics box
#
# Cite:
#
#  Stap, L.B., Van de Wal, R.S.W., de Boer, B., Koehler, P., Hoencamp,  J.H.,  Lohmann,  G.,  Tuenter,  E.,
#    and  Lourens,  L.J.: Modeled  influence  of  land  ice  and  CO2 on  polar  amplification  and  paleoclimate
#    sensitivity  during  the  past  5  million years,  Paleoceanography  and  Paleoclimatology,  33,  381-394,
#    https://doi.org/10.1002/2017PA003313, 2018
#
#  Bates, J.R.: Climate stability and sensitivity in some simple conceptual models, Climate Dynamics, 38(3-4), 455-473,
#    https://doi.org/10.1007/s00382-010-0966-0, 2012
#
# -------------------------------------------------------------------------------------------------------------------------
# Written by: L.B. Stap at Alfred-Wegener-Institut, Helmholtz-Zentrum fuer Polar- und Meeresforschung, Bremerhaven, Germany
# Email: lennert.stap<at>gmail.com
# June 2017, last change: October 2020
#--------------------------------------------------------------------------------------------------------------------------

import sys
from argparse import ArgumentParser

def parse_args():
  parser = ArgumentParser()
  parser.add_argument("-forcing", dest="forcing",type=str,
                      help='''dir with ghf files''',
                      default = None)
  parser.add_argument("--deltaQ_custom", nargs='+', dest="deltaQ_custom",
                      help='''dir with ghf files''')
  options = parser.parse_args()

  return options

def main ():

  options = parse_args()
  forcing = options.forcing
  deltaQ_custom = options.deltaQ_custom

### INPUT

# Set the forcing
  if forcing == 'homogeneous': # Homogeneous forcing, e.g. CO2
    deltaQ_NP = 4.0
    deltaQ_SP = 4.0
    deltaQ_T  = 4.0
  elif forcing == 'inhomogeneous': # Heterogeneous forcing, e.g. ice sheets
    deltaQ_NP = 12.0
    deltaQ_SP = 0.0
    deltaQ_T  = 0.0
  elif forcing == 'custom': # Custom forcing, adjust to your liking
    deltaQ_NP = float(deltaQ_custom[0])
    deltaQ_SP = float(deltaQ_custom[1])
    deltaQ_T  = float(deltaQ_custom[2])
  else:
    sys.exit("ERROR: Undefined forcing")

# Set the parameters (#values used in Stap et al. (2018))
  b_NP = 1.0 # 1.5, 1.0, 0.5
  b_SP = 1.0 # 1.5, 1.0
  b_T  = 1.5 # 1.5
  d_NP = 4.0 # 0.0, 4.0, 8.0, 9.99**99
  d_SP = 4.0 # 0.0, 4.0, 9.99**99

### MODEL CALCULATIONS

# Defining the help parameters
  alpha = b_T + d_NP + d_SP
  beta = b_NP + d_NP
  gamma = b_SP + d_SP
  S = alpha - ((d_NP**2) / beta) - ((d_SP**2) / gamma)

# Calculating temperatures, main output
  deltaT_T = (1/S) * ( deltaQ_T + ((d_NP / beta) * deltaQ_NP) + ((d_SP / gamma) * deltaQ_SP) )

  deltaT_NP = (1/S) * ( ((d_NP / beta) * deltaQ_T) +  (((d_NP**2 / beta**2) + (S / beta)) * deltaQ_NP) + ( ((d_NP * d_SP) / (beta * gamma)) * deltaQ_SP) )

  deltaT_SP = (1/S) * ( ((d_SP / gamma) * deltaQ_T) + ( ((d_NP * d_SP) / (beta * gamma)) * deltaQ_NP) + (((d_SP**2 / gamma**2) + (S / gamma)) * deltaQ_SP) )

# Calculating total radiative forcing, polar amplification and climate sensitivity
  deltaQ_total = ((deltaQ_T) + deltaQ_NP + deltaQ_SP) / 3
  deltaT_total = ((deltaT_T) + deltaT_NP + deltaT_SP) / 3
  climsens = deltaT_total / deltaQ_total
  polamp_NP = deltaT_NP / deltaT_total
  polamp_SP = deltaT_SP / deltaT_total

# OUTPUT

  print('Temperature change Northern Hemisphere:', deltaT_NP)
  print('Temperature change Southern Hemisphere:', deltaT_SP)
  print('Temperature change tropics:', deltaT_T)
  print('Temperature change global:', deltaT_total)

  print('Climate sensitivity:', climsens)
  print('Climate sensitivity double CO2:', climsens*3.7)
  print('Northern polar amplification:', polamp_NP)
  print('Southern polar amplification:', polamp_SP)

if __name__ == "__main__":
    main()
