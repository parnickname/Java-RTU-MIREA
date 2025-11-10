package practice7.ChainofResponsibility;

public class App {
    public static void main(String[] args) {
        Logger logger = LoggerFactory.createLogger();

        logger.log("INFO", "User authentication successful");
        logger.log("WARNING", "Password expires in 5 days - consider updating it");
        logger.log("ERROR", "Connection timeout to database");
    }



}
