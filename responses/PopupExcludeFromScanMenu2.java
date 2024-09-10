
package org.zaproxy.zap.extension.stdmenus;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.mock;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;

public class PopupExcludeFromScanMenuTest {

    @Test
    public void testIsSubMenu() {
        PopupExcludeFromScanMenu menu = new PopupExcludeFromScanMenu();
        assertTrue(menu.isSubMenu());
    }

    @Test
    public void testGetParentMenuName() {
        PopupExcludeFromScanMenu menu = new PopupExcludeFromScanMenu();
        assertEquals("sites.exclude.popup", menu.getParentMenuName());
    }

    @Test
    public void testPerformAction() {
        SiteNode sn = new SiteNode();
        Model modelMock = mock(Model.class);
        Session sessionMock = mock(Session.class);
        modelMock.setSession(sessionMock);

        PopupExcludeFromScanMenu menu = new PopupExcludeFromScanMenu();
        menu.performAction(sn);

    }

    @Test
    public void testPerformHistoryReferenceActions() {
        List<HistoryReference> hrefs = new ArrayList<>();
        
        PopupExcludeFromScanMenu menu = new PopupExcludeFromScanMenu();
        menu.performHistoryReferenceActions(hrefs);
        
    }

    @Test
    public void testIsSafe() {
        PopupExcludeFromScanMenu menu = new PopupExcludeFromScanMenu();
        assertTrue(menu.isSafe());
    }
}
