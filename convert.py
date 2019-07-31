import yaml, json

# Yaml Example
document = """
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: simple-ingress
  namespace: default
  annotations:
    kubernetes.io/ingress.class: "tectonic"
    ingress.kubernetes.io/rewrite-target: /
    ingress.kubernetes.io/ssl-redirect: "true"
    ingress.kubernetes.io/use-port-in-redirects: "true"
spec:
  rules:
    - host: app.apps.node.anthonydev.[fqdn]
      http:
        paths:
          - path: /
            backend:
              serviceName: simple-service
              servicePort: 80"""

y=yaml.safe_load(document);
print json.dumps(y, sort_keys=True, indent=2);

