#include <drogon/drogon.h>

int main() {
    // Carrega configuração padrão do Drogon e inicia servidor na porta 8888
    LOG_INFO << "Iniciando Charizard-Drogon C++ Web Server...";
    
    // Rota simples de health check
    drogon::app().registerHandler("/", [](const drogon::HttpRequestPtr& req, 
                                          std::function<void (const drogon::HttpResponsePtr &)> &&callback) {
        auto resp = drogon::HttpResponse::newHttpResponse();
        resp->setBody("<html><body><h1>Charizard-Drogon C++ Web Server ONLINE</h1></body></html>");
        callback(resp);
    });

    drogon::app().addListener("0.0.0.0", 8888);
    drogon::app().run();
    return 0;
}
