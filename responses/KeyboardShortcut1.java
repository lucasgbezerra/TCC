
package org.zaproxy.zap.extension.keyboard;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class KeyboardShortcutTest {

    @Test
    public void testGetName() {
        KeyboardShortcut shortcut = new KeyboardShortcut("identifier", "Test Shortcut", null);
        assertEquals("Test Shortcut", shortcut.getName());
    }

    @Test
    public void testGetIdentifier() {
        KeyboardShortcut shortcut = new KeyboardShortcut("identifier", "Test Shortcut", null);
        assertEquals("identifier", shortcut.getIdentifier());
    }

    @Test
    public void testGetKeyStroke() {
        KeyboardShortcut shortcut = new KeyboardShortcut("identifier", "Test Shortcut", null);
        assertEquals(null, shortcut.getKeyStroke());
    }

    @Test
    public void testSetKeyStroke() {
        KeyboardShortcut shortcut = new KeyboardShortcut("identifier", "Test Shortcut", null);
        shortcut.setKeyStroke(KeyStroke.getKeyStroke("control A"));
        assertTrue(shortcut.isChanged());
    }
}
