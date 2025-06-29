import * as z from "zod";

export const forgotPasswordSchema = z.object({
  email: z.string().email("Invalid email"),
});

export type ForgotPasswordFormValues = z.infer<typeof forgotPasswordSchema>;
