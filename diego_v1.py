from opentrons import simulate
metadata = {'apiLevel': '2.8'}
protocol = simulate.get_protocol_api('2.8')

plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1) #it points to a definition file of the plasticware
tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)

p300 = protocol.load_instrument('p300_multi', #defintion file
                                'right', #
                                tip_racks=[tiprack_1]) #where it takes the tips from

reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 3)

protocol.max_speeds['Z'] = 10



#Pipette buffer
p300.transfer(100, reservoir.columns()[0], plate.columns()[0:12],
              touch_tip=False, #he doesnt recommend. It touches the walls of the well to make sure all droplets fall from the tip
              blow_out=True, #second stop of the pipette
              blowout_location='destination well', #or into the trash
              new_tip='once') #if you're just transferring buffer, you might not want to change tip every time


p300.pick_up_tip()

#Pipette initial amount of fluorescein
p300.transfer(100, reservoir.columns()[1], plate.columns()[0],
             mix_after=(3,70), #twice, 50 uL each time
             touch_tip=False,
             blow_out=True,
             blowout_location='destination well',
             new_tip='never')

#Serial dilution
p300.transfer(100, plate.columns()[0:10], plate.columns()[1:11],
             mix_after=(3,70), #twice, 50 uL each time
             touch_tip=False,
             blow_out=True,
             blowout_location='destination well',
             new_tip='never')


for line in protocol.commands():
        print(line)
