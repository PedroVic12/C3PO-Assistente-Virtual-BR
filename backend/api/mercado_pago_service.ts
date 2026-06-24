import express from 'express';
import axios from 'axios';


class MercadoPagoAPI {
  private accessToken: string;
  private apiBase: string;

  constructor() {
    this.accessToken = process.env.MERCADO_PAGO_ACCESS_TOKEN || '';
    this.apiBase = 'https://api.mercadopago.com/v1';
  }

  async createPayment(paymentData: any) {
    try {
      const response = await axios.post(`${this.apiBase}/payments`, paymentData, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating payment:', error);
      throw error;
    }
  }

  async getPaymentStatus(paymentId: string) {
    try {
      const response = await axios.get(`${this.apiBase}/payments/${paymentId}`, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error getting payment status:', error);
      throw error;
    }
  }
}

class PaymentController {
  private mercadoPagoAPI: MercadoPagoAPI;

  constructor() {
    this.mercadoPagoAPI = new MercadoPagoAPI();
  }

  async processPayment(req: express.Request, res: express.Response) {
    try {
      const paymentData = req.body;
      const result = await this.mercadoPagoAPI.createPayment(paymentData);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: 'Error processing payment' });
    }
  }

  async getPaymentStatus(req: express.Request, res: express.Response) {
    try {
      const { paymentId } = req.params;
      const result = await this.mercadoPagoAPI.getPaymentStatus(paymentId);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: 'Error getting payment status' });
    }
  }
}

const app = express();
app.use(express.json());

const paymentController = new PaymentController();

app.post('/process-payment', paymentController.processPayment.bind(paymentController));
app.get('/payment-status/:paymentId', paymentController.getPaymentStatus.bind(paymentController));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});