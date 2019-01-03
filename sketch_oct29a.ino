#include <SoftwareSerial.h>

/***********************/
/* Parameters for fans */
/***********************/
int VentPin = 3;
int halfRevolutions = 0;
int prevTime = 0;
int rpm = 0;
int pwmRate = 19;

/***************************/
/* Parameters for PMS5003T */
/***************************/
byte PM5003T_DATAFRAME[32];
int PM_CONTENT[3];
int GRANULE_NUMBER[4];
int TEMPERATURE, HUMANDITY;

SoftwareSerial PMS5003T(10, 11); // RX, TX

void setup() {
	Serial.begin(9600);
	PMS5003T.begin(9600);  
	pinMode(VentPin, OUTPUT);
	pinMode(2, INPUT_PULLUP);
	attachInterrupt(0, rpmCalculation, FALLING);
	pwm25kHzBegin();
	pwmDuty(pwmRate);
}

void loop() {
	
	while(Serial.available()) {
		String s = Serial.readString();
		int dc = s.toInt();
		pwmDuty(dc+1);
	}

	airConditionRetrieve();
	pwmRate = PM_CONTENT[1] + 19;
	if(pwmRate < 99) pwmDuty(pwmRate);
	rpm = 15 * halfRevolutions;
	halfRevolutions = 0;
	String serialData = dataEncoder();
	Serial.print(serialData);
	delay(1000);
}

String dataEncoder() {
	String encodeString = "";
	for(int i = 0; i < 3; ++i) {
		encodeString += String(PM_CONTENT[i]);
		encodeString += ' ';
	}

	for(int i = 0; i < 4; ++i) {
		encodeString += String(GRANULE_NUMBER[i]);
		encodeString += ' ';
	}

	encodeString += String(TEMPERATURE);
	encodeString += ' ';
	encodeString += String(HUMANDITY);
	encodeString += ' ';
	encodeString += String(rpm);
	encodeString += '\n';
	
	return encodeString;
}

void airConditionRetrieve() {
	int i = 0;
	int CUR_PM_Pos = 10;
	int CUR_GRANULE_NUMBER_Pos = 16;
	
	while(PMS5003T.available()) {
		PM5003T_DATAFRAME[i++] = PMS5003T.read();
	}

	for(i = 0; i < 3; ++i) {
		int j = CUR_PM_Pos;
		PM_CONTENT[i] = (PM5003T_DATAFRAME[j] << 8) | PM5003T_DATAFRAME[j+1];
		CUR_PM_Pos = j + 2;
	}

	for(i = 0; i < 4; ++i) {
		int j = CUR_GRANULE_NUMBER_Pos;
		GRANULE_NUMBER[i] = (PM5003T_DATAFRAME[j] << 8) | PM5003T_DATAFRAME[j+1];
		CUR_GRANULE_NUMBER_Pos = j + 2;
	}

	TEMPERATURE = ((PM5003T_DATAFRAME[24] << 8) | PM5003T_DATAFRAME[25]) / 10;
	HUMANDITY = ((PM5003T_DATAFRAME[26] << 8) | PM5003T_DATAFRAME[27]) / 10;
}

void rpmCalculation() {
	halfRevolutions++;
}

void pwm25kHzBegin() {
	TCCR2A = 0;                               // TC2 Control Register A
	TCCR2B = 0;                               // TC2 Control Register B
	TIMSK2 = 0;                               // TC2 Interrupt Mask Register
	TIFR2 = 0;                                // TC2 Interrupt Flag Register
	TCCR2A |= (1 << COM2B1) | (1 << WGM21) | (1 << WGM20);  // OC2B cleared/set on match when up/down counting, fast PWM
	TCCR2B |= (1 << WGM22) | (1 << CS21);     // prescaler 8
	OCR2A = 99;                               // TOP overflow value (Hz)
	OCR2B = 0;
}

void pwmDuty(byte ocrb) {
	OCR2B = ocrb;                             // PWM Width (duty)
}
