/**
 * Lendo e exibindo uma imagem da camera ( Dispositivo de captura ) anexada ao computador 
 */ 
 
import processing.video.*; // importa a biblioteca de video

Capture cam; // Cria um objeto do tipo Capture

void setup() {
  size(640, 480); // Define o tamanho da janela principal

  
  cam = new Capture(this, 480, 400); // Tamanho da imagem capturada

  // Para usar uma outra camera, isto e, se o dispositivo padrao gerar um erro, 
  // lista todos os dispositivos disponiveis no console para achar sua camera
  String[] devices = Capture.list();
  println(devices);
  
  // Use devices[x] para usar a camera desejada
  cam = new Capture(this, width, height, devices[1]); // No meu notebook, devices[0] e' minha WebCam onboard, devices[1] 'e minha WebCam usb

}


void draw() {
  if (cam.available() == true) { // Verifica se a camera esta disponivel
    cam.read(); // Le a imagem
    image(cam, 0, 0,width,height); // Exibe a imagem
  }
} 
