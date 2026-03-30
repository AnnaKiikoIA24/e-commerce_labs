{{/*
Return the name of the release with suffix
*/}}
{{- define "lab4.name" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}

{{/*
Return common labels
*/}}
{{- define "lab4.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: Helm
{{- end -}}