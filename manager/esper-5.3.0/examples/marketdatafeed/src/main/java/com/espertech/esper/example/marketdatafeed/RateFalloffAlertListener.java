/**************************************************************************************
 * Copyright (C) 2006-2015 EsperTech Inc. All rights reserved.                        *
 * http://www.espertech.com/esper                                                          *
 * http://www.espertech.com                                                           *
 * ---------------------------------------------------------------------------------- *
 * The software in this package is published under the terms of the GPL license       *
 * a copy of which has been included with this distribution in the license.txt file.  *
 **************************************************************************************/
package com.espertech.esper.example.marketdatafeed;

import com.espertech.esper.client.UpdateListener;
import com.espertech.esper.client.EventBean;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class RateFalloffAlertListener implements UpdateListener
{
    public void update(EventBean[] newEvents, EventBean[] oldEvents)
    {
        if (newEvents == null)
        {
            return; // ignore old events for events leaving the window
        }

        EventBean theEvent = newEvents[0];

        log.info("Rate fall-off detected for feed=" + theEvent.get("feed").toString() +
                  " and rate=" + theEvent.get("feedCnt") +
                  " and average=" + theEvent.get("avgCnt"));
    }

    private static final Log log = LogFactory.getLog(RateFalloffAlertListener.class);
}
