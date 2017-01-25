/* Copyright 2013 Ewerton Assis.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.rmi.registry.LocateRegistry;
import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.RMISecurityManager;
import java.rmi.server.UnicastRemoteObject;

public class UpperServer extends UnicastRemoteObject implements UpperInterface {
  private String message;

  public UpperServer() throws RemoteException {
    super();
  }

  public void setMessage(String message) {
    this.message = message;
  }

  public String upperMessage() {
    return this.message.toUpperCase();
  }

  public static void main(String args[]) {
    try {
      LocateRegistry.createRegistry(2020);
      UpperInterface server = new UpperServer();
      Naming.rebind("//localhost:2020/UpperInterface", server);
      System.out.println("UpperServer is now bound in registry");
    } catch (Exception e) {
      System.out.println("UpperServer error: " + e.getMessage());
      e.printStackTrace();
    }
  }
}
