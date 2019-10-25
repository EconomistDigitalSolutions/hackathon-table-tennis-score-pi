# hackathon-table-tennis-score-pi
A raspi based Table Tennis score recorder

![](docs/logo.png)

based on: https://github.com/jujhars13/akaal-switch

## Hardware required

- Raspberry Pi B+,Zero, 3, 4 or any internet enabled Pi
- An [I2C](https://i2c.info/) enabled LCD/OLED [like this one](https://www.amazon.co.uk/gp/product/B07PWWTB94/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
- Breadboard/circuit board with wires/solder to hole the whole thing together
- Flashing Light - LED with 330Ohm resistor
- 2x Physical push switches

### Wiring Diagram

- LCD i2C SDL - `Board Pin 3`
- LCD i2C SCL - `Board Pin 5`
- Switch PullUp B - `Board Pin 36`
- Switch PullUp A - `Board Pin 37`

![wiring-diagram](docs/diagram_bb.svg)

## Todo

### Compulsory

- [ ] unwrap and setup pi
- [ ] install raspbian
- [ ] solder on pi zero header pins
- [ ] hook up pi and provision using script
- [ ] pull latest code from github at boot (github deploy key)
- [ ] draw wiring diagram (fritzing)
- [ ] hook up LED response to button press
- [ ] take photo of dev setup
- [ ] test lcd screen wireup using `i2cdetect -y 1`
- [ ] print message to LCD screen
- [ ] wire up buttons and stick to table
- [ ] stick screen and pi to table tennis table
- [ ] take photo of mvp setup
- [ ] ensure pi has autoupdates on
- [ ] re-install raspbian lite and redeploy w/ provision script
- [ ] take photo of final setup

### Optional
- [ ] solder things up to a board
