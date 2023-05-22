import Database from 'better-sqlite3';
import type { SmartDevice } from '../../utils';

const DB_PATH = './KasaSmartDevices.db'
const db = new Database(DB_PATH, { verbose: console.log });

export function getInitialDevices(): Promise<SmartDevice[]> {
  return new Promise<SmartDevice[]>((resolve, reject) => {
    let devices: SmartDevice[] = [];
  
    try {
      // Fetch all devices with their child devices
      const query = `
        SELECT s.*, c.id AS childId, c.alias AS childAlias, c.mac AS childMac
        FROM SmartDevice s
        LEFT JOIN ChildDevice c ON s.id = c.parentId
      `;
      const stmt = db.prepare(query);
      const results = stmt.all();

      // Group the results by parent device ID
      const groupedResults: Record<number, SmartDevice> = results.reduce((acc: Record<number, SmartDevice>, row: any) => {
        const { id, host, deviceType, deviceId, name, alias, mac, hasChildren, childId, childAlias, childMac } = row;
        if (!acc[id]) {
          acc[id] = {
            host,
            deviceType,
            deviceId,
            alias,
            mac,
            hasChildren,
            children: []
          };
        }

        if (childId) {
          acc[id].children.push({
            host,
            deviceType: 4,
            deviceId: childId,
            alias: childAlias,
            mac: childMac,
          });
        }

        return acc;
        }, {});

      // Convert the grouped results to an array of SmartDevice objects
      devices = Object.values(groupedResults);
      resolve(devices);
    } catch (error) {
      reject(error);
    } finally {
      // Close the database connection
      db.close();
    }
  });
}

export function insertNewDevices(devices: SmartDevice[]) {
  return new Promise<void>((resolve, reject) => {
    const insertSmartDevice = db.prepare(`
      INSERT INTO SmartDevice (host, deviceType, deviceId, name, alias, mac, hasChildren)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `);

    const insertChildDevice = db.prepare(`
      INSERT INTO ChildDevice (parentId, childId, alias)
      VALUES (?, ?, ?)
    `);

    try {
      db.transaction(() => {
        for (const device of devices) {
          // Check if the device already exists in the database
          const existingDevice = db.prepare('SELECT host FROM SmartDevice WHERE host = ?').get(device.host);

          if (existingDevice) {
            // Device already exists, skip insertion
            continue;
          }

          // Insert the parent device
          const result = insertSmartDevice.run(
            device.host,
            device.deviceType,
            device.deviceId,
            device.alias,
            device.mac,
            device.hasChildren ? 1 : 0
          );
          const parentId = result.lastInsertRowid;

          // Insert the child devices
          for (const child of device.children) {
            insertChildDevice.run(child.host, child.mac, child.alias);
          }
        }
      })();

      resolve();
    } catch (error) {
      reject(error);
    } finally {
      db.close();
    }
  });
}