import './style.css'

document.querySelector('#app').innerHTML = `
  <h1>Raspberry Pi Pico Demo</h1>
  <button class="open">Connect</button>
  <button class="write">Write</button>
  <button class="close">Disconnect</button>
`;

let port;
let reader;
let keepReading = true;
const encoder = new TextEncoder();
const decoder = new TextDecoder();

const closePort = async () => {
  await port.close();
};

const openPort = async () => {
  // Filters for Raspberry Pi Pico
  const filters = [{
    usbProductId: 5,
    usbVendorId: 11914
  }];

  // Prompt user to select any serial port.
  try {
    port = await navigator.serial.requestPort({ filters }); 
  } catch (error) {
    console.log(error);
  }

  // Wait for the serial port to open.
  try {
    await port.open({ baudRate: 115200 });
  } catch (error) {
    console.error(e);
  }

  while (port && port.readable) {
    try {
      reader = port.readable.getReader();
      for (;;) {
        const {value, done} = await reader.read();
        if (value) {
          console.log('Reader: ', decoder.decode(value));
        }
        if (done) {
          break;
        }
      }
      reader.releaseLock();
      reader = undefined;
    } catch (e) {
      console.error(e);
    }
  }
};

const writeToPort = async () => {
  console.log('write!');
  if (port?.writable == null) {
    console.warn(`unable to find writable port`);
    return;
  }

  let toFlush = '';
  const data = 'machine.Pin(25, machine.Pin.OUT).toggle()\r';

  toFlush += data;

  const encodedData = encoder.encode(data);
  console.log(encodedData);

  
  const writer = port.writable.getWriter();
  writer.write(encodedData);

  // Allow the serial port to be closed later.
  writer.releaseLock();
  toFlush = '';
};

document.querySelector('button.open').addEventListener('click', async () => {
  openPort();
  // portReader();
});

document.querySelector('button.write').addEventListener('click', async () => {
  writeToPort();
});

document.querySelector('button.close').addEventListener('click', async () => {
  closePort();
});

