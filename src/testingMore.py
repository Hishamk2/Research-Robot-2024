from bs4 import BeautifulSoup

html_text = """
"<p>I want to <strong>control multiple robots using my laptop</strong>. Robots do not have intelligence, they are sending sensor values to PC which computes the sensors values and sends back result to robots.(Centralized control of robots using PC ).</p>

<p>Robots are communicating with PC through serial communication using Zigbee mudule. </p>

<p>Problem: <strong>How to make &amp; send a structure</strong> (from robot) <strong>like {sen1, sen2,sen3..,robot id}</strong> where sen1, sen2..are sensors values and robot id is to recognize particular robot. 
After editing.....
The code I was using for sending sensors was like.</p>

<pre><code> void TxData(unsigned char tx_data)

{   SBUF = tx_data; //Transmit data that is passed to this function
     while(TI == 0); //wait while data is being transmitted
}
</code></pre>

<p>and then sending sensor values one by one</p>

<pre><code> TxData(left_whiteline_sensor);
 TI=0; // resetting transmit interrupt after each character
 TxData(middle_whiteline_sensor);
 TI=0;
 TxData(right_whiteline_sensor);
 TI=0;
 TxData(front_sharp_sensor);
 TI=0;
</code></pre>

<p>At PC end reading these values in buffer</p>

<pre><code>read(fd, buf1, sizeof(buf1));
.....
options.c_cc[VMIN]=4; // wait till not getting 4 values 
</code></pre>

<p>This was <strong>working fine</strong> when there was <strong>only one robot</strong>, now as we have <strong>multiple robots</strong> and each robot is sending data using above function, I am <strong>getting mixed sensor values</strong> of all robots of <strong>at PC end</strong>. One solution is to <strong>make a structure</strong> which I mentioned above and send it to PC. This is what I want to ask ""<strong>How to make and send such a structure</strong>""
Sorry for not framing question correctly before.</p>

<p>Thanks...</p>
"

""" 

soup = BeautifulSoup(html_text, 'html.parser')
readable_text = soup.get_text() 
print(readable_text) 