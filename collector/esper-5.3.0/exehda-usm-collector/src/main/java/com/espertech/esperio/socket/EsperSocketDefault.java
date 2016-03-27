package com.espertech.esperio.socket;

import com.espertech.esper.client.Configuration;
import com.espertech.esper.client.EPServiceProvider;
import com.espertech.esper.client.EPServiceProviderManager;
import com.espertech.esper.client.EPStatement;
import com.espertech.esper.client.EventBean;
import com.espertech.esper.client.EventType;
import com.espertech.esper.client.SafeIterator;
import com.espertech.esper.client.StatementAwareUpdateListener;
import com.espertech.esper.client.UnmatchedListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

import java.io.IOException;
import java.util.List;
import java.util.Properties;

public class EsperSocket {

    public static class CEPListener implements StatementAwareUpdateListener {

        private String tag;
        private static final String EVENT_TYPE = "eventType";

        public CEPListener(String tag) {
            this.tag = tag;
        }

        @Override
        public void update(EventBean[] newEvents, EventBean[] oldEvents, EPStatement eps, EPServiceProvider epsp) {
            String situation = new String();
//            SafeIterator<EventBean> safeIter = eps.safeIterator();
//            situation = situation.concat(eps.getText() + "^");
            try {
            	EventType eventType = null;
//                for (; safeIter.hasNext();) {
                for (EventBean event : newEvents) {
//                    EventBean event = safeIter.next();
                    eventType = event.getEventType();
//                    System.out.println(eventType.getName());
                    for (String propertyName : eventType.getPropertyNames()) {
                        if (!EVENT_TYPE.equals(propertyName)) {
                            situation = situation.concat("[" + propertyName + "=" + event.get(propertyName) + "]");
                        }
                    }
                    situation = situation.concat("|");

                }
//                if (!eventType.getName().contains("Log")) {
//                	situation = eventType.getName() + "^" + situation;
//                } else {
                	situation = eps.getText() + "^^" + situation;
//                }
                situation = situation.substring(0, situation.length() - 1);
            } finally {
//                safeIter.close();
                System.out.println(situation);
            }

        }
    }

    public static void main(String[] args) throws IOException, InterruptedException {

        File itemsProperty = new File(args[0]);
        int port = new Integer(args[1]);

        String esperIOConfig = "<esperio-socket-configuration>\n"
                + "<socket name=\"service1\" port=\"" + port + "\" data=\"csv\"/>"
                + "</esperio-socket-configuration>";

        Configuration engineConfig = new Configuration();
        
//        engineConfig.getEngineDefaults().getThreading().setInternalTimerEnabled(false);
        engineConfig.getEngineDefaults().getExecution().setPrioritized(true);
        engineConfig.addPluginLoader("EsperIOSocketAdapter", EsperIOSocketAdapterPlugin.class.getName(), new Properties(), esperIOConfig);

        BufferedReader itemFile
                = new BufferedReader(new FileReader(itemsProperty));
        String dataRow = itemFile.readLine();

        while (dataRow != null) {
            String[] dataArray = dataRow.split("&");
            String className = new String();

            String propertyNamesAux = null;
            int i = 0;
            while (dataArray.length > i) {
//            	System.out.println("Item: " + dataArray[i]);

                // Confirma o primeiro valor como nome da "classe"
                if (dataArray[i].startsWith("!")) {
                    String[] propertyNames = null;
                    Object[] propertyTypes = null;
                    className = dataArray[i].substring(1, dataArray[i].length() - 1); // Para remover o !

                    // O termo propriedades a seguir pode ser entendido como colunas ou campos de cada evento
                    // Passa para os nomes das propriedades (a serem utilizadas nas consultas EPL) 
                    i = i + 1;
                    propertyNames = dataArray[i].split(",");

                    // Passa para os tipos dos dados associados a cada propriedade (observar ordem de acordo 
                    // com os nomes das propriedades)
                    i = i + 1;
                    propertyTypes = dataArray[i].split(",");

//                    System.out.println("ClassName: " + className);
//                    int aux = 0;
//                    while (propertyNames.length > aux) {
//                        System.out.println("Property Name: " + propertyNames[aux]);
//                        System.out.println("Property Type: " + propertyTypes[aux]);
//                        aux++;
//                    }
                    engineConfig.addEventType(className, propertyNames, propertyTypes);

                }
                i = i + 1;
            }
            dataRow = itemFile.readLine();
        }
        itemFile.close();

        EPServiceProvider provider = EPServiceProviderManager.getProvider("SocketAdapterTest", engineConfig);

        // Statements
        //  end statements
        provider.getEPRuntime().setUnmatchedListener(new UnmatchedListener() {
            @Override
            public void update(EventBean eb) {
                String simpleEvent = new String();
                EventBean newEvent = eb;
                String EVENT_TYPE = "eventType";
                EventType eventType = newEvent.getEventType();
                if (!eventType.getName().contains("Log")) {
                	simpleEvent = simpleEvent.concat(eventType.getName() + "~");
                    for (String propertyName : eventType.getPropertyNames()) {
                        if (!EVENT_TYPE.equals(propertyName)) {
                            simpleEvent = simpleEvent.concat("[" + propertyName + "=" + newEvent.get(propertyName) + "]");
                        }
                    }
                    System.out.println(simpleEvent);
                }                
            }
        });

        Object lock = new Object();
        synchronized (lock) {
            lock.wait();
        }
    }
}
